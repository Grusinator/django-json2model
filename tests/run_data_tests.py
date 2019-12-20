import json
import os

import django
from django.test import TransactionTestCase

from json2model.services.dynamic_model import (
    create_instances_from_json,
    create_objects_from_json
)

test_data_path = "./tests/test_data"
test_data_results_path = "./tests/test_data_results"


def run_test_on_data(file):
    data = get_test_data(file)
    data = data[:10]
    expected = get_test_data_results(file)
    create_objects_from_json("root_obj0", data)
    inst = create_instances_from_json("root_obj0", data)


def get_test_data_results(file):
    try:
        return json.load(open(os.path.join(test_data_results_path, file)))
    except FileNotFoundError:
        pass


def get_test_data(file):
    return json.load(open(os.path.join(test_data_path, file)))


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
                run_test_on_data(file)
