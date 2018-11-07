from data import * 
import web_crawler
from web_crawler import DataType
import link_analysis
import time
    

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
    a = ModelData()
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
    print(Links.objects.all())
    print(time.time())
        


if __name__ == '__main__':
    check_links_in_database()