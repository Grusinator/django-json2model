from json2model.services.dynamic_model.dynamic_model_mutant import DynamicModelMutant


def create_objects_from_json(root_name, data):
    return DynamicModelMutant.create_models_from_data(root_name, data)


def create_instances_from_json(root_name, data):
    return DynamicModelMutant.create_instances_from_data(root_name, data)