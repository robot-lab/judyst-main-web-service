

export function GetRandomStr(size) {
    return Math.random().toString(36).substring(size);   
}

export function  GetRandomInt(min, max) {
    var rand = min - 0.5 + Math.random() * (max - min + 1)
    rand = Math.round(rand);
    return rand;
}