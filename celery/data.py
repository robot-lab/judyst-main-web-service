
import django
import os
import sys

sys.path.append('../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "judyst_web_service.settings")
django.setup()

from judyst_web_service import settings
from django.db import models
from core.models import *


class ModelData(object):

    def __init__(self):
        self.__models_dict = {
            "Documents": Documents,
            "CustomUser": CustomUser,
            "Links": Links
        }

    def get_data(self, data_field, model_name=None, **kwargs):
        """
        получить значение поля {data_field} из строки из {data_base}
        соответствующей условию {**kwargs}

        :param data_field: str
            поле из базы данных информацию из корого надо получить

        :param model_name: str
            имя модели с которой надо работать

        :param kwargs: field="str"
            условие для выбора подходящей строки, допустим:
            doc_id="КСРФ/2-П/2007"

        :return: data_field value
            возвращает значение из этого поля строки удовлетворяющей условию
        """
        data_base = self.__models_dict.get(model_name)
        if data_base is None:
            return None
        model = None
        result = None
        try:
            model = data_base.objects.get(**kwargs)
            result = getattr(model, data_field)
        except data_base.DoesNotExist:
            # print(f'no such model exist {model_name}')
            pass
        except Exception as e:
            print(e)

            print(f"something went wrong, may be not correct {kwargs}")
        return result

    def get_all_data(self, data_field, model_name=None):
        """
        функция для получения значения поля {data_field} из всех строк таблицы

        :param data_field: str
            наименование этого поля

        :param model_name: str
            имя модели с которой надо работать

        :return: List
            всех значений этого поля в таблице
        """
        result = []
        data_base = self.__models_dict.get(model_name)
        if data_base is None:
            return None
        try:
            for model in data_base.objects.all():
                result.append(getattr(model, data_field))
        except Exception:
            print("no such field in table")
        return result

    def create_data(self, model_name=None, **kwargs):
        """
        функция для того что бы создать строку с этой информацией в таблицу

        :param model_name: str
            имя модели с которой надо работать

        :param kwargs: field1="str", field2="str"
            информация которую надо добавить

        :return: None
        """
        data_base = self.__models_dict.get(model_name)
        if data_base is None:
            return None
        try:
            model = data_base.objects.create(**kwargs)
            model.save()
        except Exception as e:
            print(e)

            print(f"something went wrong, may be not correct {kwargs}")

    def edit_data(self, data, model_name=None, **kwargs):
        """
        функция для того что бы редактировать строку с этой информацией
        в таблицу

        :param data: {"field1":"str", "field2":"str"}
            информация которую надо добавить

        :param model_name: str
            имя модели с которой надо работать

        :param kwargs: field="str"
            условие для выбора подходящей строки, допустим:
            doc_id="КСРФ/2-П/2007"

        :return: None
        """
        data_base = self.__models_dict.get(model_name)
        if data_base is None:
            return None
        try:
            model = data_base.objects.get(**kwargs)
            for key, value in data.items():
                setattr(model, key, value)
            model.save()
        except Exception as e:
            print(e)

            print(f"something went wrong, may be not correct {kwargs}")


if __name__ == '__main__':
    # a = ModelData(CustomUser)
    # print(a.get_data("email", "CustomUser", username="korwin@mail.ru"))
    # a.create_data("CustomUser", username="levozavr@mail.ru",
    #                email="levozavr@mail.ru", password="aaaassss")
    # a.edit_data({"email": "lev@mail.ru"}, "CustomUser",
    #               username="korwin@mail.ru")
    # print(a.get_all_data("email", "CustomUser"))
    a = ModelData()
    import web_crawler
    from web_crawler import DataType
    import link_analysis
    import time
    # Coping local file base into database
    # source = web_crawler.ksrf_models.LocalFileStorageSource()
    # source.folder_path = './tmp/programming/Judyst/files'
    # source.prepare()
    # databaseSource = web_crawler.\
    #                  ksrf_models.KSRFDatabaseWrapper('KSRFDatabase', a)
    # web_crawler.tools.updatae_database_from_source(databaseSource, source)
   
    # checking documents in database
    # print(time.time())
    # databaseSource = web_crawler.\
    #                  ksrf_models.KSRFDatabaseWrapper('KSRFDatabase', a)
    # print(databaseSource.get_all_data(DataType.DOCUMENT_HEADER))
    # print(databaseSource.get_data('КСРФ/2476-О/2018', DataType.DOCUMENT_TEXT))
    # print(time.time())

    # collecting links in Result folder
    # print(time.time())
    # source = web_crawler.\
    #     ksrf_models.\
    #     KSRFDatabaseWrapper('KSRFDatabase', a)
    # link_analysis.Init(source)
    # link_analysis.process_period(
    #     firstDateOfDocsForProcessing='18.03.1900',
    #     lastDateOfDocsForProcessing='14.08.2019',
    #     docTypesForProcessing={'КСРФ/О', 'КСРФ/П'},
    #     firstDateForNodes='18.03.2014', lastDateForNodes='14.08.2017',
    #     nodesIndegreeRange=(0, 25), nodesOutdegreeRange=(0, 25),
    #     nodesTypes={'КСРФ/О', 'КСРФ/П'},
    #     includeIsolatedNodes=False,
    #     firstDateFrom='18.03.2016', lastDateFrom='14.08.2016',
    #     docTypesFrom={'КСРФ/О', 'КСРФ/П'},
    #     firstDateTo='18.03.2015', lastDateTo='14.08.2015',
    #     docTypesTo={'КСРФ/О', 'КСРФ/П'},
    #     weightsRange=(1, 5),
    #     showPicture=False, sendRequestToUpdatingHeadersInBaseFromSite=False,
    #     takeHeadersFromLocalStorage=False)

    # print(time.time())
    
    # print(time.time())

    # put links in database
    print(time.time())
    source = web_crawler.\
        ksrf_models.\
        KSRFDatabaseWrapper('KSRFDatabase', a)
    links = link_analysis.converters.load_json('Results/cleanLinks.json')
    source.put_data_collection(links, DataType.LINK)
    print(time.time())


    #check links in database
    # print(time.time())
    # print(Links.objects.all())
    # print(time.time())
        