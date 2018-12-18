from data import * 
import web_crawler
from web_crawler import DataType
import link_analysis
import time
import os
    

def update_database_from_localstorage(
        fileStoragePath='./tmp/programming/Judyst/files'):
    a = ModelData()
    source = web_crawler.ksrf_models.LocalFileStorageSource()
    source.folder_path = fileStoragePath
    source.prepare()
    databaseSource = web_crawler.\
                     ksrf_models.KSRFDatabaseWrapper('KSRFDatabase', a)
    web_crawler.tools.updatae_database_from_source(databaseSource, source)


def check_documents_in_database():
    print(time.time())
    databaseSource = web_crawler.\
                     ksrf_models.KSRFDatabaseWrapper('KSRFDatabase', a)
    print(databaseSource.get_all_data(DataType.DOCUMENT_HEADER))
    print(databaseSource.get_data('КСРФ/2476-О/2018', DataType.DOCUMENT_TEXT))
    print(time.time())


def collect_links_and_save_in_folder():
    a = ModelData()
    print(time.time())
    source = web_crawler.\
        ksrf_models.\
        KSRFDatabaseWrapper('KSRFDatabase', a)
    link_analysis.Init(source)
    link_analysis.process_period(
        firstDateOfDocsForProcessing='18.03.1900',
        lastDateOfDocsForProcessing='14.08.2019',
        docTypesForProcessing={'КСРФ/О', 'КСРФ/П'},
        firstDateForNodes='18.03.2014', lastDateForNodes='14.08.2017',
        nodesIndegreeRange=(0, 25), nodesOutdegreeRange=(0, 25),
        nodesTypes={'КСРФ/О', 'КСРФ/П'},
        includeIsolatedNodes=False,
        firstDateFrom='18.03.2016', lastDateFrom='14.08.2016',
        docTypesFrom={'КСРФ/О', 'КСРФ/П'},
        firstDateTo='18.03.2015', lastDateTo='14.08.2015',
        docTypesTo={'КСРФ/О', 'КСРФ/П'},
        weightsRange=(1, 5),
        showPicture=False, sendRequestToUpdatingHeadersInBaseFromSite=False,
        takeHeadersFromLocalStorage=False)
    print(time.time())


def put_links_in_database():    
    a = ModelData()
    print(time.time())
    source = web_crawler.\
        ksrf_models.\
        KSRFDatabaseWrapper('KSRFDatabase', a)
    links = link_analysis.converters.load_json('Results/cleanLinks.json')
    source.put_data_collection(links, DataType.LINK)
    print(time.time())


def check_links_in_database():
    print(time.time())
    links = Links.objects.all()
    print(f' count: {len(links)}')
    print(time.time())
        

def fill_database_from_files(tasks):
    print(time.time())
    a = ModelData()    
    wrapper = web_crawler.DatabaseWrapper('db_source', a)
    for task in tasks:
        web_crawler.tools.fill_data_source_from_file(
            wrapper, task['filename'], dataType=task['dataType'],
            fileFormat=task['fileFormat'])
    print(time.time())


if __name__ == '__main__':
    tasks = [
            #   {
            #   'filename': 'files/TestHeaders.json',
            #   'dataType': DataType.DOCUMENT_HEADER,
            #   'fileFormat': 'json'
            #   },             
            #   {
            #   'filename': 'files/Codecs_cleanLinks.json',
            #   'dataType': DataType.LINK,
            #   'fileFormat': 'json'
            #   },
               {
                'filename': 'files/codeHeaders.jsonlines',
                'dataType': DataType.DOCUMENT_HEADER,
                'fileFormat': 'jsonlines'
              },
              {
              'filename': 'files/ACTESTTexts.jsonlines',
              'dataType': DataType.DOCUMENT_TEXT,
              'fileFormat': 'json'
              },

              

              ]
    # fill_database_from_files(tasks)
    # update_database_from_localstorage()
    print(Documents.objects.count)