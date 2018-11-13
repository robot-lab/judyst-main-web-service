function trimFromSpaces(arr){
    return arr.map(function(item){
        return item.trim();
    }).filter(function(item){
        if (item !== '')
            return item;
    });
}

function distinctArr(arr) { 
    return arr.filter(function (value, index, self)
    {
        return self.indexOf(value) === index;
    });
}



export default {trimFromSpaces, distinctArr};
