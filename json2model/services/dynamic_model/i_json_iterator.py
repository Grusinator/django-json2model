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
    def _iterate_data_structure(cls, data, object_label=None, parent_label=None):
        if isinstance(data, list):
            return cls._handle_list_data(parent_label, object_label, data)
        cls.handle_object(parent_label, object_label, data)
        attributes, related_objects = cls._split_into_attributes_and_related_objects(data)
        cls._handle_attributes(object_label, attributes)
        cls._handle_related_objects(object_label, related_objects)
        return object_label

    @classmethod
    def _handle_list_data(cls, parent_label, object_label, data):
        if not any(cls.list_element_is_objects(data)):
            return cls.handle_attribute_lists(parent_label, object_label, data)
        elif all(cls.list_element_is_objects(data)):
            [cls.handle_related_object(parent_label, object_label, inner_data) for inner_data in data]
            return object_label
        else:
            raise NotImplementedError("i dont know what kind of obscure mixed types of lists can occur")

    @classmethod
    def _handle_attributes(cls, parent_name, data: dict):
        return [cls.handle_attribute(parent_name, label, data) for label, data in data.items()]

    @classmethod
    def _handle_related_objects(cls, parent_label, data):
        return {label: cls.handle_related_object(parent_label, label, inner_data) for label, inner_data in data.items()}

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

    @classmethod
    def list_element_is_objects(cls, data):
        return list(map(lambda x: isinstance(x, dict), data))
