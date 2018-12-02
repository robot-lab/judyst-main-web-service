from core.models import Links, Documents
from datetime import datetime
from core.serializers import document_serializer
from core.utils.exceptions import BadSearchRequestException


id_types = {1: 'supertype', 2: 'interredaction_id', 3:  'doc_id'}


def get_id_type(doc_id):
    """
    check doc_id and get number of id type (index of id_types)
    :param doc_id: str 
        id from search request
    :return: int
    """
    parts = doc_id.split('/')
    id_type = len(parts)
    if id_type not in id_types:
        raise BadSearchRequestException()
    return id_type


def get_sql_by_id(doc_id, side):
    """
    form and return sql request for getting all matching links
    :param doc_id: str
        pattern to match, can be supertype,
        interredaction id or exact doc_id
    :param side: str
        to or from, side of link arrow
    :return: str 
        valid sql request as str
    """
    id_type = id_types[get_id_type(doc_id)]
    sql = f'select * from {Links.objects.model._meta.db_table} where '
    if id_type == 'doc_id':
        id_type += '_' + side
        sql += f"{id_type} = '{doc_id}'"
        return sql
    if id_type == 'supertype':
        sql += f"doc_id_{side} in (select doc_id from \
                 {Documents.objects.model._meta.db_table} where (supertype = '{doc_id}'))"
        return sql
    if id_type == 'interredaction_id':
        sql += f"doc_id_{side} in (select doc_id from \
                 {Documents.objects.model._meta.db_table} where (interredaction_id = '{doc_id}'))"
        return sql
    raise Exception('Impossible!')


def intersect_sql_requests(sql1, sql2):
    """
    form sql as intersection given requests
    :param sql1: str
        first sql
    :param sql2: str
        second sql
    :return: str
        valid sql
    """
    return f'{sql1} intersect {sql2}'


def get_links(validate_data):
    """
    function for getting links from db

    :param validate_data: Dict
         validate data from request

    :return: queryset
        queryset of Links model
    """
    if validate_data['doc_id_from'] != -1 and\
            validate_data['doc_id_to'] != -1:
        sql = intersect_sql_requests(
                get_sql_by_id(validate_data['doc_id_to'], 'to'),
                get_sql_by_id(validate_data['doc_id_from'], 'from'))
        queryset = Links.objects.raw(sql)
    elif validate_data['doc_id_from'] != -1:
        sql = get_sql_by_id(validate_data['doc_id_from'], 'from')
        queryset = Links.objects.raw(sql)
    elif validate_data['doc_id_to'] != -1:
        sql = get_sql_by_id(validate_data['doc_id_to'], 'to')
        queryset = Links.objects.raw(sql)
    else:
        queryset = Links.objects.all()
    return queryset


def get_document_by_id(validate_data):
    """
    function for getting document from db by unique id.

    :param validate_data: Dict
         validate data from request

    :return: document
         Document model
    """
    document = Documents.objects.get(doc_id=validate_data['doc_id'])
    return document_serializer(document)


def get_document_by_interredaction_id(validate_data):
    """
    function for getting document from db by interredaction id.

    :param validate_data: Dict
         validate data from request

    :return: document
         Document model
    """
    documents = Documents.objects.filter(
        interredaction_id=validate_data['doc_id'])
    if documents:
        document = None
        ids = []
        for doc in documents:
            ids.append(doc.doc_id)
            if not document:
                document = doc
            else:
                if doc.effective_date:
                    new_date = datetime.strptime(doc.effective_date,
                                                 '%d.%m.%Y')
                    old_date = datetime.strptime(document.effective_date,
                                                 '%d.%m.%Y')
                    if datetime.now() > new_date > old_date:
                        document = doc

        serializable_document = document_serializer(document)
        serializable_document['editions'] = ids
        return serializable_document
    else:
        return None
