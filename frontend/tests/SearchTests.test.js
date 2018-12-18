import search_utils from './../src/SearchAlgorithms/utils.js';
import search from '../src/SearchAlgorithms/search.js';
import citationsFuncs from '../src/SearchAlgorithms/citations.js';

import delimiters from '../src/SearchAlgorithms/delimiters';
import marks from '../src/SearchAlgorithms/marks';

import {GetRandomStr, GetRandomInt} from './utils';
import Search from '../src/SearchAlgorithms/search.js';

const CitationFastSearch = citationsFuncs.CitationFastSearch; 

const cicleCount = 10; 
const id_size_min = 2;
const id_size_max = 10; 

const id_count_min = 1;
const id_count_max = 10; 

const count_rand_arr_min = 0; 
const count_rand_arr_max = 10; 
for (let i = 0; i < 10*cicleCount; i++ )
{
    expect.extend({toBeDistincted(received){
        let res = true; 
        for(let i = 0; i < received.length; i++)
        {
            if (received.indexOf(received[i]) != i)
            {
                res = false; 
                break;
            }
        }

        if (res)
            return {
                message: "all elems unique",
                pass: true
            }
        else
            return{
                message: "there is equal elems",
                pass: false
            }
    }})  ;
    describe('distinct test '+ i, ()=>{
        let arr = []; 
        for (let j = 0; i < GetRandomInt(count_rand_arr_min, count_rand_arr_max); i++ )
            arr.push(GetRandomStr(j));
        it('no repeated elem', ()=>{
            expect(search_utils.distinctArr(arr)).toBeDistincted();
        });
        it('with repeated elem', ()=>{
            const cnt = GetRandomInt(arr.length);
            for (let j = 0; j < cnt; j ++)
            {
                arr.push(arr[i]);
            }
            expect(search_utils.distinctArr(arr)).toBeDistincted();
        });
        
    })
}




for (let i = 0; i < cicleCount; i++ )
{
    describe(`simple citation and search test ${i}` ,()=>{
        const idFrom = GetRandomStr(GetRandomInt(id_size_min, id_size_max)); 
        const idTo = GetRandomStr(GetRandomInt(id_size_min, id_size_max)); 
        it('id to id', ()=>{
            const searchReq = `${idFrom} ${delimiters.CitationPartsDelimiter} ${idTo}`;
            const expected = [{doc_id_from: idFrom, doc_id_to: idTo}];
            expect( CitationFastSearch(searchReq)).toEqual(expect.arrayContaining(expected));  
            expect(Search(searchReq)).toEqual(expect.arrayContaining(expected)); 
        });




        it('any to id', ()=>{
            const searchReq = `${marks.any_front} ${delimiters.CitationPartsDelimiter} ${idTo}`;
            const expected = [{doc_id_from: marks.any_back, doc_id_to: idTo}];
            expect( CitationFastSearch(searchReq)).toEqual(expect.arrayContaining(expected));   
            expect(Search(searchReq)).toEqual(expect.arrayContaining(expected)); 
        });
        
        it('id to any', ()=>{
            const searchReq = `${idFrom} ${delimiters.CitationPartsDelimiter} ${marks.any_front}`;
            const expected = [{doc_id_from: idFrom, doc_id_to: marks.any_back}];
            expect( CitationFastSearch(searchReq)).toEqual(expect.arrayContaining(expected));   
            expect(Search(searchReq)).toEqual(expect.arrayContaining(expected)); 
        });

        it('any to any', ()=>{
            const searchReq = `${marks.any_front} ${delimiters.CitationPartsDelimiter} ${marks.any_front}`;
            const expected = [{doc_id_from: marks.any_back, doc_id_to: marks.any_back}];
            expect( CitationFastSearch(searchReq)).toEqual(expect.arrayContaining(expected));   
            expect(Search(searchReq)).toEqual(expect.arrayContaining(expected)); 
        });

        
    })
}

for (let i = 0; i < cicleCount; i++ )
{
    describe(`|| citation test ${i}` ,()=>{
        const countFrom = GetRandomInt(id_count_min, id_count_max);
        const countTo = GetRandomInt(id_count_min, id_count_max);

        let idsFrom = [];
        let  idsTo = [];
        for (let i = 0; i < countFrom; i++)
        {
            idsFrom.push(GetRandomStr(GetRandomInt(id_size_min, id_size_max)));
        }
        for (let i = 0; i < countTo; i++)
        {
            idsTo.push(GetRandomStr(GetRandomInt(id_size_min, id_size_max)));
        }
        idsFrom = search_utils.distinctArr(idsFrom);
        idsTo = search_utils.distinctArr(idsTo);

        it('many id to many id', ()=>{
            const searchReq = `${idsFrom.join(delimiters.ElemsDelimiter )}` + 
                          `${delimiters.CitationPartsDelimiter}` +
                          `${idsTo.join(delimiters.ElemsDelimiter)}`;
            const expected = []; 
            for (i = 0; i < idsFrom.length; i++)
                for (var j = 0; j < idsTo.length; j++)
                    expected.push({doc_id_from: idsFrom[i], doc_id_to: idsTo[j]});    
            
            expect(CitationFastSearch(searchReq)).toEqual(expect.arrayContaining(expected));
        });

        it('any id to many id', ()=>{
            const searchReq = `${marks.any_front}` + 
                          `${delimiters.CitationPartsDelimiter}` +
                          `${idsTo.join(delimiters.ElemsDelimiter)}`;
            const expected = []; 
            for (var j = 0; j < idsTo.length; j++)
                expected.push({doc_id_from: marks.any_back, doc_id_to: idsTo[j]});    
            
            expect(CitationFastSearch(searchReq)).toEqual(expect.arrayContaining(expected));
        });

        it('many id to any id', ()=>{
            const searchReq = `${idsFrom.join(delimiters.ElemsDelimiter )}` + 
                          `${delimiters.CitationPartsDelimiter}` +
                          `${marks.any_front}`;
            const expected = []; 
            for (i = 0; i < idsFrom.length; i++)
                expected.push({doc_id_from: idsFrom[i], doc_id_to: marks.any_back});    
            
            expect(CitationFastSearch(searchReq)).toEqual(expect.arrayContaining(expected));
        });
    });
}



