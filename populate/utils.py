# utils.py by Raunak
#
# A framework to safely populate data on different servers with
#   universal utility methods for population scripts
#
# handles issues like:
#   Integrity Errors in DB
#   Duplicates flooding
#   Purging changes on demand

class ItemCreator(object):
    verbose = True # verbose setting for static/classonly methods
    def __init__(self, model, fields, fields_default_values=None, replace=True, verbose=True):
        """
        @param: model: django.db.models.Model => Model for which objects are to be created
        @param: fields: list/dict => list/dict of model accepted fields
        @param: fields_default_values: dict => dict of default field values
        @param: replace: bool => indicates whether to replace an existing model instance
            with provided data
        @param: verbose: bool => indicates if print statements will run during calls
        """
        self.model = model
        self.fields = fields
        self.fields_default_values = fields_default_values
        self.verbose = verbose
        self.list_created_objects = [] # keeps track of all obejcts created in db

    def create(self, data, push_defaults=True):
        """Creates object in db"""
        return self._create(data, True, push_defaults)

    def create_virtual(self, data, push_defaults=True):
        """Creates virtual object without saving in db"""
        return self._create(data, False, push_defaults)

    def save(self, obj, overwrite=True):
        """
        Saves object to DB while trying to avoid DB integrity errors
        @param: obj: Model_instance => object to be saved
        @param: overwrite: bool => indicated whether to overwrite existing object in DB
        """
        data = self.serialize_obj(self.fields, obj)
        if not data: # checking if object's data and fields are inconsistent
            if self.verbose:
                print "Object is inconsistent with provided fields: {}. Can't save!".format(self.fields)
            return False

        try: # checking if object already exists in DB
            fetched_obj = self.model.objects.get(**data) # getting similar object from db
            if self.verbose:
                print "Object already exists in db: {}.".format(fetched_obj)
            if not overwrite:
                if self.verbose:
                    print "Returning fetched object.".format(fetched_obj)
                return fetched_obj
        except self.model.DoesNotExist:
            pass

        if self.verbose:
            print "Saving object: {}.".format(obj)

        return self.model.objects.update_or_create(**data)[0]

    def purge_all(self, created_only=False):
        """
        Deletes all objects created/fetched during the process depending on created_only
        @param: created_only: bool => True implies delete items which were created but not fetched
        """
        for obj in self.list_created_objects:
            _obj, created = obj
            if self.created_only and (not created):
                if self.verbose:
                    print "Skipping deleting fetched object: {}".format(_obj)
                continue
            if self.verbose:
                print "Deleting object: {}".format(_obj)
            obj.delete()
        self.list_created_objects = []

    def validate_data(self, data, push_defaults=True):
        """
        @param: data: dict => dict of field keys and values
        @param: push_defaults: bool => indicates if deafaults are to be supplied for absent fields
        Ensures all kwargs provided are acceptable field names and there are no None values
        Also fills any kwargs not provided by default values
        """
        for key, value in data.iteritems():
            if not key in self.fields:#PopulateUser.USER_FIELDS_DEF
                if self.verbose:
                    print "Unexpected key found: %s"%(key)
                return None
            if value == None:
                if self.verbose:
                    print "None value found for key: %s"%(key)
                return None
        _data = {}
        if self.fields_default_values and push_defaults:
            _data = dict(self.fields_default_values)#PopulateUser.USER_FIELDS_DEF
        _data.update(data)
        return _data

    @staticmethod
    def serialize(key_list, value_list):
        """
        Serializes key and value lists into key-value pair dictionary
        @param: key_list: list => list of fields to be serialized
        @param: value_list: list => list of values to be serialized
        """
        if len(key_list) != len(value_list):
            if ItemCreator.verbose:
                print "Serialization falied! key and value lists have different" +\
                        " number of elements {}, {}".format(key_list, value_list)
            return None
        return {key:value for key, value in zip(key_list, value_list)}

    @staticmethod
    def serialize_obj(key_list, obj, accept_broken=False):
        """
        Serializes object into key and value pairs dict where keys are lsited by key_list
        @param: key_list: list => list of fields to be serialized
        @param: obj: object => object to be serialized
        @param: accept_broken: bool => Will return incomplete serialization even if a key
            isn't found on object
        """
        _serialized = {}
        for key in key_list:
            try:
                _serialized[key] = getattr(obj, key)
            except AttributeError as e:
                if ItemCreator.verbose:
                    print "Object {} doesn't have attribute: {}".format(obj, key)
                if not accept_broken:
                    return None
        return _serialized

    def _create(self, data, save, push_defaults=True):
        """Creates object (virtual or in db as per save setting)"""
        data = self.validate_data(data, push_defaults)
        if not data:
            if self.verbose:
                print "Error occured in data validation. Unable to create object."
            return None
        obj = None
        try:
            if save:
                print "Creating/Fetching object: {} with data: {}".format(self.model, data)
                obj = self.model.objects.get_or_create(**data)
                self.list_created_objects.append(obj)
                obj = obj[0]
            else:
                obj = self.model(**data)
        except Exception as e:
            if self.verbose:
                print "Exception occured while trying to create object of Model: " +\
                        "%s with data: %s"%(self.model, data)
                print "Probably the given model or field definitions need to be rechecked!"
                print e
        return obj
