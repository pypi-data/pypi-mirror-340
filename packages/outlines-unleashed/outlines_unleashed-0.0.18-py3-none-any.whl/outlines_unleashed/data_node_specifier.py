import json
from abc import ABC, abstractmethod


def data_node_specifier_factory(version, dns_structure):
    if version == "0.1":
        from outlines_unleashed.data_node_specifier_v0_1 import DataNodeSpecifier_v0_1
        return DataNodeSpecifier_v0_1(dns_structure)
    if version == "0.2":
        from outlines_unleashed.data_node_specifier_v0_2 import DataNodeSpecifier_v0_2
        return DataNodeSpecifier_v0_2(dns_structure)

    raise ValueError(f"Unsupported version: {version}")


class BaseDataNodeSpecifier(ABC):
    def __init__(self, dns_structure):
        """
        Initialises the DND based on an input data structure which defines the fields to be extracted and the
        criteria to be used to locate each field.

        :param dns_structure:
        """
        self.dns_structure = dns_structure
        self._validate_data_node_specifier()

    @classmethod
    def from_json_file(cls, json_path):
        with open(json_path, 'r') as json_fp:
            json_object = json.load(json_fp)

            return cls.from_json_object(json_object)

    @classmethod
    def from_json_string(cls, serialized_specifier):
        """
        Overloaded function which will take one of:
        - A string containing a JSON representation of a DND
        - File object for a file containing a JSON representation of a DND
        - A file path to a file containing a JSON representation of a DND

        The function will parse the JSON according to which version of the JSON format is encapsulated, and
        create a new DND object.
        :return:
        """
        specifier_json_object = json.loads(serialized_specifier)

        return cls.from_json_object(specifier_json_object)

    @staticmethod
    def to_json(descriptor):
        """
        Takes a full descriptor (with header) and converts it to a json string.

        Tries to use common code for all versions of the descriptor structure, but where there
        is a need for specific logic for a given version it will be included.

        :param descriptor:
        :return:
        """
        # Note this is a fairly generic approach which may not work as structure evolves.
        serialized_descriptor = json.dumps(descriptor, default=lambda o: o.__dict__, indent=4)

        return serialized_descriptor

    @abstractmethod
    def _validate_data_node_specifier(self):
        pass

    @classmethod
    @abstractmethod
    def from_json_object(cls, json_object):
        pass

    @abstractmethod
    def extract_data_node(self, data_node, override_data_node_tag_delim=False):
        pass




