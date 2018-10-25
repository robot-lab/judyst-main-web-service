from core.utils.functions import create_link_from_fields
import json


def get_dict_from_user(user):
    """
    Function for getting dict from user model.

    :param user: user
        Object of user model for serialization

    :return: dict
        Dict with user fields for checking.
    """
    return {'first_name': user.first_name, 'last_name': user.last_name,
            'email': user.email, 'username': user.username, 'id': user.id,
            'organization': user.organization}


def get_dict_from_link(link):
    """
    Function for getting dict from link.

    :param link: Link
        Link for casting.

    :return: Dict
        Dict with Link fields for checking.
    """
    return {'doc_id_from': link.doc_id_from, 'doc_id_to': link.doc_id_to,
            'to_doc_title': link.to_doc_title,
            'citations_number': link.citations_number,
            'contexts_list': link.contexts_list,
            'positions_list': link.positions_list, 'id': link.id}


def set_links_in_db_from_list(links):
    """
    Function for setting links to db from list.

    :param links: list
        List of dicts, describing links.

    :return: int
        Number of inserted links.
    """
    result = 0
    for link in links:
        create_link_from_fields(link)
        result += 1
    return result


def set_links_in_db_from_file(file_name):
    """
    Function for inserting links in db from file.

    :param file_name: str
        File path for parsing.

    :return: int
        Number of inserted links.
    """
    with open(file_name, "r", encoding="UTF-8") as f_in:
        links = json.load(f_in)
        return set_links_in_db_from_list(links)


def is_equal_lists(list1, list2):
    """
    Function for checking if list1 and list2 equal.
    :param list1: list
        First list for checking.
    :param list2: list
        Second list for checking.
    :return:
        True if equal, False otherwise.
    """
    if not isinstance(list1, list) or not isinstance(list2, list):
        raise TypeError
    for elem1 in list1:
        flag = False
        for i, elem2 in enumerate(list2):
            if list2[i] == elem1:
                del list2[i]
                flag = True
                break
        if not flag:
            return False
    return not list2


user_fields = {'email': 'goodEmail@gmail.com',
               'password': '#########12345[]%&',
               'first_name': 'name', 'last_name': 'surname',
               'organization': 'My organisation'}


login_fields = {'email': 'badEmail@gmail.com', 'password': 'p4thw3450rd'}

default_user_fields = {'email': 'badEmail@gmail.com',
                       'password': 'p4thw3450rd',
                       'first_name': 'name', 'last_name': 'surname',
                       'organization': 'My organisation'}

link_fields = {'doc_id_from': 'КСРФ/36-п/2018', 'doc_id_to': 'КСРФ/4-П/1996',
               'to_doc_title': 'много текста\nочень много текста\xa0',
               'citations_number': 1,
               'contexts_list': ['много тескста 2\nсовсем много текста\x0c5'],
               'positions_list': [7918]}
