import Citations from "./citations.js";
import Delimiters from './delimiters.js';
import Keywords from './keywords.js';


function ExtendedSearch()
{
    throw 'Not implemented!';    
}

function Search(searchRequest)
{   
    var keys = Keywords.values;

    for (var element in keys)
        if (searchRequest.indexOf(element) !== -1)
                return ExtendedSearch(searchRequest);

    if (searchRequest.indexOf(Delimiters.CitationPartsDelimiter))
        return Citations.CitationFastSearch(searchRequest);

    throw 'Not implemented!';    
}


export default Search;