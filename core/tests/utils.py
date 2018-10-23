def get_dict_from_user(user):
    """
    Function for getting json from user model.

    :param user: user
        Object of user model for serialization

    :return: str
        String with json of user.
    """
    return {'first_name': user.first_name, 'last_name': user.last_name,
            'email': user.email, 'username': user.username, 'id': user.id,
            'organization': user.organization}


user_fields = {'email': 'goodEmail@gmail.com', 'password': '12345',
               'first_name': 'name', 'last_name': 'surname',
               'organization': 'My organisation'}


login_fields = {'email': 'badEmail@gmail.com', 'password': 'p4thw0rd'}

default_user_fields = {'email': 'badEmail@gmail.com', 'password': 'p4thw0rd',
                       'first_name': 'name', 'last_name': 'surname',
                       'organization': 'My organisation'}
