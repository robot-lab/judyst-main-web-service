import Citations from "./citations";
import Delimiters from './delimiters';
import Keywords from './keywords';


function ExtendedSearch()
{
    throw 'Not implemented!';    
}

function Search(searchRequest)
{   
    var keys = Keywords.values();

    for (var element in keys)
        if (searchRequest.indexOf(element) !== -1)
                return ExtendedSearch(searchRequest);

    if (searchRequest.indexOf(Delimiters.CitationPartsDelimiter))
        return Citations.CitationFastSearch(searchRequest);

    throw 'Not implemented!';    
}


export default Search;