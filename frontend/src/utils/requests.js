import Search from '../SearchAlgorithms/search.js';


function RequestLinks(range, url, searchResults, callback)
{
  var peakedLinksCount = 0; 
  var i = 0;
  var startedCoutnter = 0; 
  var finishedCounter = 0; 
  var links = []
  
  var get = function (range, searchResult) {
      
      var req = {doc_id_from: searchResult.doc_id_from,
                 doc_id_to: searchResult.doc_id_to,
                 range: range}
      var jsonReq = JSON.stringify(req);
      var xhr = new XMLHttpRequest();
      xhr.open('POST', url, true);
      xhr.setRequestHeader("content-type", "application/json");
      
      xhr.send(jsonReq);

      xhr.onreadystatechange = function(){
          if (this.readyState != 4) return;
          if (this.status != 200) {
              alert( 'ошибка: ' + (this.status ? this.statusText : 'запрос не удался') );
              return;
          }
          var json = xhr.responseText;
          var linkList = JSON.parse(json);
          var ret = []
          for (var i = 0; i < linkList.length; i ++)
              ret.push({id: i, Link: linkList[i]});
          links = links.concat(ret);
          finishedCounter++;
      }
  }
  while (i < searchResults.length && peakedLinksCount < range[0])
  {
      if (peakedLinksCount + searchResults[i].Size <= range[0])
      {
          peakedLinksCount += searchResults[i].Size;
          i++;
      }
      else
      {
          var min_point = range[0] - peakedLinksCount;
          if (peakedLinksCount + searchResults[i].Size <= range[1])
          {
              var currRange = [min_point, searchResults[i].Size]
              peakedLinksCount += searchResults[i].Size; 
          }
          else
          {
              var max_point =  range[1] - peakedLinksCount ;
              currRange = [min_point, max_point ]; 
              peakedLinksCount += range[1] - range[0]; 
          }
          startedCoutnter++;
          var j = i; 
          setTimeout(function(){
              
              get(currRange, searchResults[j]);},0);
          i++;
          break;
      }

  }
  while (i < searchResults.length && peakedLinksCount < range[1])
  {
      if (peakedLinksCount + searchResults[i].Size <= range[1])
      {
          
          currRange = [0, searchResults[i].Size];
          peakedLinksCount += searchResults[i].Size;
          
      }
      else
      {
          currRange = [0, range[1] - peakedLinksCount]
          peakedLinksCount = range[1]
      }
      j = i;
      setTimeout(function(){get(currRange, searchResults[j]);},0);
      startedCoutnter++;
      i++;
  }
  var checker = function(){
      if (startedCoutnter <= finishedCounter)
      {

          callback(links);
      }
      else
      setTimeout(checker, 500);
  };
  setTimeout(checker, 0);
}



function RequestSearch(request, url, callback)
{
    var requests = Search(request);
    if (requests == null)
    {
        callback(null);
        return;
    }
    var rets = [];
    var counter = 0;
    for (var i = 0; i < requests.length; i++)
    {
        var req = requests[i];

        var jsonReq = JSON.stringify(req);
        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.setRequestHeader("content-type", "application/json")
        
        xhr.send(jsonReq)
        xhr.onreadystatechange = function () {
            if (this.readyState != 4) return;
            if (this.status != 200) {
                //console.log( 'ошибка: ' + (this.status ? this.statusText : 'запрос не удался') );
                counter += 1;
                return;
            }
            var json = this.responseText + '';
            var linkCount = JSON.parse(json)
            rets.push({Size: linkCount.size, doc_id_from: req.doc_id_from, doc_id_to: req.doc_id_to})
            counter += 1; 
        }

    }

    var waiter = function(){
        if (counter === requests.length)
            {
              callback(rets);
            }
        else
            setTimeout(waiter, 500);
    }
    setTimeout(waiter, 500);                

}


function RequestDocument(doc_id, url, callback)
{
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.setRequestHeader("content-type", "application/json")
    var jsonReq = JSON.stringify({doc_id: doc_id});
    xhr.send(jsonReq);
    xhr.onreadystatechange = function () {
        if (this.readyState != 4) return;
        if (this.status != 200) {
            //console.log( 'ошибка: ' + (this.status ? this.statusText : 'запрос не удался') );
            callback(null);
            return;
        }
        var json = this.responseText + '';
        var document = JSON.parse(json);
        callback(document);
    };
}



export default {
    RequestLinks,
    RequestSearch,
    RequestDocument,

}