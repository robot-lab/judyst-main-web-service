import stash_chars from './stash_chars.js';

function Hash(str)
{
    var hash = 0, i, chr;
    if (str.length === 0) return hash;
    for (i = 0; i < str.length; i++) {
        chr   = str.charCodeAt(i);
        hash  = ((hash << 5) - hash) + chr;
        hash |= 0; // Convert to 32bit integer
    }
    return hash;
}


function HashLink(link)
{
    return Hash(`${link.doc_id_from}${link.doc_id_to}`);
}


function StashDocId(docId)
{
    return docId.split(stash_chars.doc_id_delimiter[0]).join(stash_chars.doc_id_delimiter[1]);
}


function DeStashDocId(docId)
{
    return docId.split(stash_chars.doc_id_delimiter[1]).join(stash_chars.doc_id_delimiter[0]);
}


function StashRequest(searchRequest)
{
    searchRequest = searchRequest.split(stash_chars.doc_id_delimiter[0]).join(stash_chars.doc_id_delimiter[1]);
    return searchRequest;
}


function DeStashRequest(searchRequest)
{
    searchRequest = searchRequest.split(stash_chars.doc_id_delimiter[1]).join(stash_chars.doc_id_delimiter[0]);
    return searchRequest;
}




// fillContexts: function(links)
        // {
        //     for (var i = 0; i < links.length; i++)
        //     {
        //         var link = links[i];
        //         link.contexts = []
        //         for(var j = 0; j < link.positions_list.length; j++)
        //         {
        //             var position = link.positions_list[j]
        //             var before = link.text.substr(position.context_start,
        //                                             position.link_start - position.context_start)
        //             var citation = link.text.substr(position.link_start,
        //                                             position.link_end - position.link_start)
        //             var after = link.text.substr(position.link_end,
        //                                             position.context_end - position.link_end)
                    
        //             var context = {before: before, citation: citation, after: after}
        //             // this.tmp = link.positions_list[j]
        //             link.contexts.push(context)

        //         }
        //         links[i] = link
        //     }
        //     return links
        // },


export default{
    Hash,
    StashDocId,
    DeStashDocId,
    HashLink,
    StashRequest,
    DeStashRequest,
    
}