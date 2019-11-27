from json2model.services.dynamic_model.dynamic_model_mutant import DynamicModelMutant


def create_objects_from_json(root_name, data):
    return DynamicModelMutant.create_models_from_data(root_name, data)

def get_dynamic_model(model_name):
    return DynamicModelMutant.get_dynamic_model(model_name)

def create_instances_from_json(root_name, data):
    return DynamicModelMutant.create_instances_from_data(root_name, data)