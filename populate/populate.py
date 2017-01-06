# populate.py by Raunak
#
# Will populate some basic data
# A superuser with username and password == root
# A normal user with username and password == user, email == user@gmail.com
#
# Has strong measures against overwriting and integrity errors

from utils import ItemCreator
from settings import SETUP_SETTINGS


class PopulateUser(object):
    # Default User model to be accessed
    USER_FIELDS = [  # #User field names
        "username",
        "password",
        "email",
        "first_name",
        "is_superuser",
        "is_active",
        "is_staff",
    ]
    USER_FIELDS_DEF = [  # Default User field values in same order as USER_FIELDS
        "user",
        "pass",
        "user@dummy.com",
        "test_user",
        False,
        False,
        False,
    ]
    SUPER_USER_DEF = [  # Default superuser field values
        "root",
        "root",
        "super@dummy.com",
        "test_super",
        True,
        True,
        True,
    ]

    def __init__(self, model=None):
        """
        @param: model: django model of a User. When nothing is provided, default django model is used
        """
        if not model:
            # importing default django model for User
            from django.contrib.auth.models import User
            model = User
        # Serializing default user field values and saving
        PopulateUser.USER_FIELDS_DEF = ItemCreator.serialize(PopulateUser.USER_FIELDS,
                                                             PopulateUser.USER_FIELDS_DEF)
        # Serializing default superuser field values and saving
        PopulateUser.SUPER_USER_DEF = ItemCreator.serialize(
            PopulateUser.USER_FIELDS,
            PopulateUser.SUPER_USER_DEF)
        self.creator = ItemCreator(
            model, PopulateUser.USER_FIELDS_DEF, PopulateUser.USER_FIELDS_DEF)

    def create_user(self, username, password, email, f_name,
                    is_super=False, is_active=False, is_staff=False):
        """
        Create a user with specified State
        @param: username: string NOT NULL
        @param: password: string NOT NULL
        @param: email: string NOT NULL
        @param: f_name: string NOT NULL; first name of user
        @param: is_super: bool DEF False; marks a user as a superuser
        @param: is_active: bool DEF False; marks user as active
        @param: is_staff: bool DEF False; marks user as staff and be able to user admin site
        """
        _data = [username, password, email,
                 f_name, is_super, is_active, is_staff]
        data = self.creator.serialize(PopulateUser.USER_FIELDS, _data)
        return self.creator.create(data)

    def create_default_superuser(self, **kwargs):
        """
        Creates a Superuser, i.e. an Admin with default field values while updating
            them with any values provided in kwargs
        Avoids duplication as much as possible
        """
        # creating a copy of default superuser values
        data = dict(PopulateUser.SUPER_USER_DEF)
        data.update(kwargs)
        password = data["password"]  # password can't be set by create
        del data["password"]
        super_ = self.creator.create(data, push_defaults=False)
        super_.set_password(password)
        super_.save()
        return super_

    def create_default_user(self, **kwargs):
        """
        Creates a user with default field values while updating them with any values
            provided in kwargs
        Avoids duplication as much as possible
        """
        # creating a copy of default user values
        data = dict(PopulateUser.USER_FIELDS_DEF)
        data.update(kwargs)
        password = data["password"]  # password can't be set by create
        del data["password"]
        user_ = self.creator.create(data, push_defaults=False)
        user_.set_password(password)
        user_.save()
        return user_


def main():
    import os
    os.environ.setdefault(*SETUP_SETTINGS)
    import django
    django.setup()
    p_user = PopulateUser()
    print p_user.create_default_user()
    print p_user.create_default_superuser()


if __name__ == "__main__":
    main()
