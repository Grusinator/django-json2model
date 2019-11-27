from abc import ABCMeta, abstractmethod


class IJsonIterator:
    __metaclass__ = ABCMeta

    att_types = (str, int, float, bool)

    @classmethod
    @abstractmethod
    def handle_attribute(cls, parent_name: str, label: str, data):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def handle_attribute_lists(cls, parent_name: str, label: str, data):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def handle_object(cls, parent_name: str, label: str, data):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def handle_related_object(cls, parent_name: str, label: str, data):
        raise NotImplementedError

    @classmethod
    def _iterate_data_structure(cls, object_name, data):
        if isinstance(data, list):
            return cls._handle_list_data(object_name, data)
        cls.handle_object(None, object_name, data)
        attributes, related_objects = cls._split_into_attributes_and_related_objects(data)
        cls._handle_attributes(object_name, attributes)
        cls._handle_related_objects(object_name, related_objects)
        return object_name

    @classmethod
    def _handle_list_data(cls, object_name, data):
        if not any(map(lambda x: isinstance(x, dict), data)):
            return cls.handle_attribute_lists(None, object_name, data)
        elif all(map(lambda x: isinstance(x, dict), data)):
            # TODO we need some more info here, what is the parent?
            return cls._handle_related_objects(object_name, data)
        else:
            # i dont know what kind of obscure mixed types of lists can occur
            raise NotImplementedError

    @classmethod
    def _handle_attributes(cls, parent_name, data: dict):
        return [cls.handle_attribute(parent_name, label, data) for label, data in data.items()]


    @classmethod
    def _handle_related_objects(cls, parent_name, data):
        return {label: cls.handle_related_object(parent_name, label, inner_data) for label, inner_data in data.items()}

    @classmethod
    def _split_into_attributes_and_related_objects(cls, data):
        properties = {}
        related_instances = {}
        for name, value in data.items():
            if isinstance(value, (dict, list)):
                related_instances[name] = value
            else:
                properties[name] = value

        return properties, related_instances
