import utils from './utils';
import delimiters from './delimiters';
import marks from './marks';

function FastCitationSearch(requestString)
{
    var sreq = requestString.split(delimiters.CitationPartsDelimiter);
    sreq = utils.trimFromSpaces(sreq);
    if (sreq.length < 2)
        return null;
    var idsFrom = sreq[0].split(delimiters.ElemsDelimiter);
    idsFrom = utils.trimFromSpaces(idsFrom);
    idsFrom = utils.distinctArr(idsFrom);
    var idsTo = sreq[1].split(delimiters.ElemsDelimiter);
    var requests = [];
    idsTo = utils.trimFromSpaces(idsTo);
    idsTo = utils.distinctArr(idsTo);
    
    if (idsFrom.indexOf(marks.any) !== -1)
    {    if (idsTo.indexOf(marks.any) !== -1)
        {
            return null; // TODO let getting out all links. 
        }
        else
        {
            for(var i = 0; i < idsTo.length; i++)
            {
                requests.push({doc_id_from: marks.any, doc_id_to: idsTo[i]});
            }
        }
    } else
    {
        if (idsTo.indexOf(marks.any) !== -1)
        {
            for(i = 0; i < idsFrom.length; i++)
            {
                requests.push({doc_id_from: idsFrom[i], doc_id_to: marks.any});
            }
        }
        else
        {
            for (i = 0; i < idsFrom.length; i++)
                for (var j = 0; j < idsTo.length; j++)
                    requests.push({doc_id_from: idsFrom[i], doc_id_to: idsTo});
        }
    }
    return requests;
}


export default {
    FastCitationSearch,
}
