# encoding: utf-8
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
    a = ModelData()
    # print(a.get_data("email", "CustomUser", username="korwin@mail.ru"))
    # a.create_data("CustomUser", username="levozavr@mail.ru",
    #                email="levozavr@mail.ru", password="aaaassss")
    # a.edit_data({"email": "lev@mail.ru"}, "CustomUser",
    #               username="korwin@mail.ru")
    # print(a.get_all_data("email", "CustomUser"))
    print(Documents.objects.count)
    pass