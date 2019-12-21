import json
import os

import django
from django.db.models import Model
from django.test import TransactionTestCase

from json2model.services.dynamic_model import (
    create_instances_from_json,
    create_objects_from_json
)

test_data_path = "./tests/test_data"
test_data_results_path = "./tests/test_data_results"


def build_test_file_path(file):
    return os.path.join(test_data_path, file)


def try_read_json_file(file):
    try:
        return json.load(open(file))
    except FileNotFoundError:
        pass


def write_to_file(data, file):
    with open(file, 'w') as outfile:
        outfile.write(str(data))


def build_result_file_path(file):
    test_data_results_file = os.path.join(test_data_results_path, file)
    test_data_results_file = test_data_results_file.replace(".json", "_results.json")
    return test_data_results_file


def create_dict_from_inst(instance):
    inst_dict = instance.__dict__
    inst_dict.pop("_state")
    for key, value in inst_dict.items():
        if isinstance(value, Model):
            related_dict = create_dict_from_inst(value)
            inst_dict[key] = related_dict
    return inst_dict


def instances_to_list_of_json(instances):
    # TODO this serializer should be made better, use django_generic_serializer
    if isinstance(instances, Model):
        return [create_dict_from_inst(instances)]
    elif isinstance(instances, list):
        return [create_dict_from_inst(instance) for instance in instances]


class TestOnJsonData(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestOnJsonData, cls).setUpClass()
        django.setup()

    def test_all_files(self):
        import os
        for file in os.listdir(test_data_path):
            if file.endswith(".json"):
                self.run_test_on_data(file)

    def run_test_on_data(self, file):
        test_file_path = build_test_file_path(file)
        data = try_read_json_file(test_file_path)
        test_data_results_file = build_result_file_path(file)
        expected = try_read_json_file(test_data_results_file)
        root_name = file.replace(".json", "_root_obj")
        create_objects_from_json(root_name, data)
        instances = create_instances_from_json(root_name, data)
        instances_json = instances_to_list_of_json(instances)
        if expected:
            self.assertListEqual(instances_json, expected)
        else:
            write_to_file(json.dumps(instances_json, indent=4), test_data_results_file)
