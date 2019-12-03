from abc import ABC, abstractmethod

from json2model.services.dynamic_model import DynamicModelMutant
from json2model.services.dynamic_model.i_json_iterator import IJsonIterator


class DynamicDataInstances(IJsonIterator, ABC):

    @classmethod
    def create_instances_from_data(cls, root_label, data):
        object_name = cls._iterate_data_structure(data, object_label=root_label)
        return

    @classmethod
    @abstractmethod
    def handle_attribute(cls, object_ref: str, label: str, data):
        """This method is for dealing with each attribute that gets identified in the tree including lists of
        attributes"""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def pre_handle_object(cls, parent_ref: str, object_label: str, data):
        """do what ever you must with the current object that has been identified"""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def post_handle_object(cls, parent_ref: str, object_label: str, data):
        """do what ever you must with the current object, but after creation of the relation and attributes"""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def handle_related_object(cls, parent_ref: str, label: str, data, parent_has_many: bool = False):
        """This method is called after exiting the iteration of the related object, so the relation can be handled
        after both objects has been handled"""
        raise NotImplementedError


    @classmethod
    def _create_object_instance(cls, model_def, related_instances: dict, properties: dict):
        Model = model_def.model_class()
        if isinstance(related_instances, list):
            pass
        return Model.objects.create(**properties, **related_instances)

