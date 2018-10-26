
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "judyst_web_service.settings")
django.setup()

from judyst_web_service import settings
from django.db import models
from core.models import *


class ModelData(object):

    def __init__(self, data_base):
        self.__data_base = data_base

    def get_data(self, data_field, **kwargs):
        """
        получить значение поля {data_field} из строки из {data_base}
        соответствующей условию {**kwargs}

        :param data_field: str
            поле из базы данных информацию из корого надо получить

        :param kwargs: field="str"
            условие для выбора подходящей строки, допустим:
            doc_id="КСРФ/2-П/2007"

        :return: data_field type
            возвращает значение из этого поля строки удовлетворяющей условию
        """
        model = None
        result = None
        try:
            model = self.__data_base.objects.get(**kwargs)
            result = getattr(model, data_field)
        except model.DoesNotExist:
            print('no such model exist')
        except Exception:
            print("something went wrong, may be not correct params")
        return result

    def get_all_data(self, data_field):
        """
        функция для получения значения поля {data_field} из всех строк таблицы

        :param data_field: str
            наименование этого поля

        :return: List
            всех значений этого поля в таблице
        """
        result = []
        try:
            for model in self.__data_base.objects.all():
                result.append(getattr(model, data_field))
        except Exception:
            print("no such field in table")
        return result

    def put_data(self, **kwargs):
        """
        функция для того что бы добавить эту информацию в таблицу

        :param kwargs: field1="str", field2="str"
            информация которую надо добавить

        :return: Тщту
        """
        try:
            model = self.__data_base.objects.create(**kwargs)
            model.save()
        except Exception:
            print("something went wrong, may be not correct params")


if __name__ == '__main__':

    a = ModelData(CustomUser)
    print(a.get_data("email", username="korwin@mail.ru"))