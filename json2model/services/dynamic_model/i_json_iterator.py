from abc import ABCMeta, abstractmethod




class IJsonIterator:
    __metaclass__ = ABCMeta

    JSON_ATTRIBUTE_TYPES = (str, int, float, bool)

    @classmethod
    @abstractmethod
    def handle_attribute(cls, parent_name: str, label: str, data):
        """This method is for dealing with each attribute that gets identified in the tree including lists of
        attributes"""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def handle_object(cls, parent_name: str, label: str, data):
        """do what ever you must with the current object that has been identified"""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def handle_related_object(cls, parent_name: str, label: str, data, parent_has_many: bool = False):
        """This method is called after exiting the iteration of the related object, so the relation can be handled
        after both objects has been handled"""
        raise NotImplementedError

    @classmethod
    def _iterate_data_structure(cls, data, object_label=None, parent_label=None):
        cls.handle_object(parent_label, object_label, data)
        attributes, one2one_related_objs, one2many_related_objs = cls._split_into_attributes_and_related_objects(data)
        cls._handle_attributes(object_label, attributes)
        cls._handle_one2one_related_objects(object_label, one2one_related_objs)
        cls._handle_one2many_related_objects(object_label, one2many_related_objs)
        return object_label

    @classmethod
    def _handle_attributes(cls, parent_name, data: dict):
        return [cls.handle_attribute(parent_name, label, data) for label, data in data.items()]

    @classmethod
    def _handle_one2one_related_objects(cls, parent_label, data):
        return {label: cls._inner_handle_related_object(parent_label, label, inner_data) for label, inner_data in
                data.items()}

    @classmethod
    def _handle_one2many_related_objects(cls, parent_label, data):
        for object_label, objects in data.items():
            for object_data in objects:
                cls._inner_handle_related_object(parent_label, object_label, object_data, parent_has_many=True)

    @classmethod
    def _inner_handle_related_object(cls, parent_label, object_label, data, parent_has_many: bool = False):
        related_object = cls._iterate_data_structure(data, object_label=object_label, parent_label=parent_label)
        cls.handle_related_object(parent_label, object_label, data, parent_has_many=parent_has_many)
        return related_object

    @classmethod
    def _split_into_attributes_and_related_objects(cls, data):
        # TODO create unit test
        properties = {}
        one2one_related_objects = {}
        one2many_related_objects = {}
        for name, value in data.items():
            # only one2one relations are selected here
            if isinstance(value, dict):
                one2one_related_objects[name] = value
            # if it is a list it will either be an attribute or a one2many relation, and we dont deal with that here.
            elif isinstance(value, list):
                if not any(cls.list_element_is_objects(value)):# and all([type(val) in ATTRIBUTE_TYPES for val in value]):
                    properties[name] = value
                elif all(cls.list_element_is_objects(value)):
                    one2many_related_objects[name] = value
                else:
                    raise NotImplementedError("i dont know what kind of obscure mixed types of lists can occur "
                                              "(fx objects and values)")
            elif isinstance(value, cls.JSON_ATTRIBUTE_TYPES):
                properties[name] = value
            else:
                raise NotImplementedError("the list contains not known attribute data types")
        return properties, one2one_related_objects, one2many_related_objects

    @classmethod
    def list_element_is_objects(cls, data):
        return list(map(lambda x: isinstance(x, dict), data))
