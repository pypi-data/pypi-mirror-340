import copy
from typing import Optional

from outlines_unleashed.data_node_specifier import BaseDataNodeSpecifier
from outlines_unleashed.node_ancestry_matching_criteria import NodeAncestryMatchingCriteria


class DataNodeSpecifier_v0_2(BaseDataNodeSpecifier):
    """
    Implements more sophisticated version of the data node specifier to increase flexibility in how data tables
    are generated from the outline.
    """

    def _validate_data_node_specifier(self):
        pass

    @classmethod
    def from_json_object(cls, json_object):
        specifier = {'header': json_object['header'], 'descriptor': {}}

        # Add the text and note tag regex delimiters.
        # ToDo: Develop clear rules for the value to use for tag delimiters to indicate not specified etc.
        text_tag_delimiter_left = json_object['header']['tag_delimiters']['text_delimiters'][0]
        text_tag_delimiter_right = json_object['header']['tag_delimiters']['text_delimiters'][1]
        note_tag_delimiter_left = json_object['header']['tag_delimiters']['note_delimiters'][0]
        note_tag_delimiter_right = json_object['header']['tag_delimiters']['note_delimiters'][1]

        specifier['header']['tag_delimiters'] = {}
        specifier['header']['tag_delimiters']['text_delimiters'] = [text_tag_delimiter_left, text_tag_delimiter_right]
        specifier['header']['tag_delimiters']['note_delimiters'] = [note_tag_delimiter_left, note_tag_delimiter_right]

        raw_descriptor = json_object['descriptor']

        specifier['descriptor']['field_extractors'] = []

        for raw_field_extractor in raw_descriptor['field_extractors']:
            field_extractor = {}
            field_extractor['field_name'] = raw_field_extractor['field_name']
            field_extractor['field_locators'] = []
            for raw_field_locator in raw_field_extractor['field_locators']:
                field_locator = {}

                field_locator['field_value_specifier'] = raw_field_locator['field_value_specifier']

                # If field value specifier is CONSTANT then we need the actual constant value to be present
                if field_locator['field_value_specifier'] == "CONSTANT":
                    if 'field_value' in raw_field_locator:
                        field_locator['field_value'] = raw_field_locator['field_value']
                    else:
                        # For now, rather than raise exception, just set default value
                        field_locator['field_value'] = "UNDEFINED_VALUE"
                field_locator['ancestry_matching_criteria'] = []
                criteria_list = raw_field_locator['ancestry_matching_criteria']
                for criteria_set in criteria_list:
                    criteria_object = NodeAncestryMatchingCriteria(
                        child_number=criteria_set.get('child_number', None),
                        text=criteria_set.get('text', None),
                        note=criteria_set.get('note', None),
                        text_tag=criteria_set.get('text_tag', None),
                        note_tag=criteria_set.get('note_tag', None),
                    )
                    field_locator['ancestry_matching_criteria'].append(criteria_object)
                field_extractor['field_locators'].append(field_locator)
            specifier['descriptor']['field_extractors'].append(field_extractor)

        return cls(specifier)

    @staticmethod
    def _key_field_check(primary_key_filter, primary_key_flag):
        if primary_key_filter is None:
            return True
        elif primary_key_filter is True and primary_key_flag == True:
            return True
        elif primary_key_filter is False and primary_key_flag == False:
            return True
        else:
            return False

    def _extract_field_names(self, primary_key_only: Optional[bool] = None):
        field_descriptors = self.dns_structure['header']['field_descriptors']

        fields = [
            field_name for field_name in field_descriptors
            if self._key_field_check(primary_key_only, field_descriptors[field_name]['primary_key'])
        ]
        return fields

    @staticmethod
    def _initialise_data_node_record(field_list):
        return {key: None for key in field_list}

    def _cleanup_extracted_record(self, data_node_record):
        """
        The record is passed in after all fields that are in the data node have been extracted.  This method
        then checks for fields which weren't populated and gives them the default value for the field, taken
        from the data node specifier.

        :param data_node_record:
        :return:
        """
        for field in data_node_record:
            if data_node_record[field] is None:
                data_node_record[field] = self._extract_field_default_value(field)

    def _extract_field_default_value(self, field_name):
        """
        Mainly needed when a data node is being extracted and there isn't a sub-node which matches a particular field. The
        record will need a value for each field which is specified and the specifier for a field allows a default value
        to be specified.  If none is specified then None is returned.

        :param field_name:
        :return:
        """
        descriptor = self.dns_structure['descriptor']
        field_specifier = descriptor[field_name]
        if 'default_value' in field_specifier:
            return field_specifier['default_value']
        else:
            return None

    def extract_data_node(self, data_node, override_data_node_tag_delim=False):
        """

        :param data_node:
        :param override_data_node_tag_delim:
        :return:
        """
        if override_data_node_tag_delim:
            # We are overriding the tag delimiters from the data node with those from the DNS.
            delimiters = self.dns_structure['header']['tag_delimiters']

            data_node.tag_regex_text = tuple(delimiters['text_delimiters'])
            data_node.tag_regex_note = tuple(delimiters['note_delimiters'])

        match_list = self._match_data_node(data_node)
        data_node_table = []
        primary_key_field_list = self._extract_field_names(primary_key_only=True)
        non_primary_key_field_list = self._extract_field_names(primary_key_only=False)

        # Initialise record for first row
        data_node_record = self._initialise_data_node_record(primary_key_field_list+non_primary_key_field_list)

        for match in match_list:
            field_name, field_value = match
            if data_node_record[field_name] is None:
                data_node_record[field_name] = field_value
            else:
                # We have already populated this field, so either it's a new primary key value (end of record)
                # or an error.
                if field_name in primary_key_field_list:
                    # A primary key field is about to be overwritten.
                    # There are a few cases to process here:
                    # - Current record must be complete now so can be written (all cases I think)
                    # - If this is not the last primary key field of the set then we have effectively
                    #   moved to a new branch and so we need to blank out any key fields in the data record
                    #   we are constructing as well as all non-key fields
                    # - Any fields which aren't populated will trigger a warning and an appropriate
                    #   default value assigned.

                    self._cleanup_extracted_record(data_node_record)

                    # Append copy of record to output table so don't keep updating same pointer.
                    data_node_table.append(copy.deepcopy(data_node_record))

                    # Now update new primary key field as part of next record.
                    data_node_record[field_name] = field_value

                    # If this field isn't the last key field in the primary key, then blank out deeper
                    # elements within the current data node record as it doesn't apply to the new branch.
                    key_index = [index for index, value in enumerate(primary_key_field_list) if value == field_name]

                    assert (len(key_index) == 1)
                    if key_index[0] < len(primary_key_field_list) - 1:
                        # Key field which isn't last one has changed so need to blank out deeper key
                        # values in the data node record as they should be re-filled from next branch
                        # of node tree.

                        for index in range(key_index[0] + 1, len(primary_key_field_list)):
                            data_node_record[primary_key_field_list[index]] = None

                    # Initialise record for next row.  Key fields should be maintained apart from the one which has
                    # changed. So just initialise non key fields and then update current key field.
                    for field_name in non_primary_key_field_list:
                        data_node_record[field_name] = None
                else:
                    # New value for non-primary key field.  That's an error (but only a warning to be issued)
                    # ToDo: Add logging to allow warnings to be issued which don't stop programme.
                    pass

        # All data fields have been processed, so just clean up the final record and add to the list.
        self._cleanup_extracted_record(data_node_record)
        data_node_table.append(copy.copy(data_node_record))

        return data_node_table

    def _match_data_node(self, unleashed_node):
        """
        Treat the supplied node as the root of a data node embedded within a larger outline structure.  Using the
        field_specifications provided identify all nodes within the data_node sub-tree structure which match
        the supplied criteria, and extract the information required to fully define each extracted field

        :param unleashed_node:
        :return: Information required to create a field object for each matched field and construct records
                 from the fields.
        """
        override_node = self._override_tag_regex(unleashed_node)
        match_list = []
        for data_node_list_entry in override_node.iter_unleashed_nodes():
            for matched_field_data in self._match_field_node(data_node_list_entry):
                match_list.append(matched_field_data)

        return match_list

    def _match_field_node(self, field_node_list_entry):
        """
        Look for one or more fields within a supplied candidate field node.

        A node could contain more than one field as there are four places within a node where a field
        could live and it is possible to create criteria which match the same node but extract a different
        value.

        This function is built as a generator to continue to return values until there are no more
        matches to look for.

        :param field_node_list_entry:
        :return:
        """
        descriptor = self.dns_structure['descriptor']

        # Descriptor is a list of field_extractors, each of which matches a specific node attribute to a specific
        # output field.  But there can be multiple field_extractors for each field if a field can be populated
        # in more than one way (so for business requirements the level field is populated from the level 2
        # and level 3 nodes (or something like that!)

        field_extractors = descriptor['field_extractors']

        for field_extractor in field_extractors:
            field_name = field_extractor['field_name']
            for field_locator in field_extractor['field_locators']:
                criteria = field_locator['ancestry_matching_criteria']
                if self._match_field(field_node_list_entry, criteria):
                    field_value = self._extract_field(field_node_list_entry.node(), field_locator)
                    yield field_name, field_value

    @staticmethod
    def _extract_field(field_node, field_criteria):
        """
        Extracts the field value from the node according to the field_specifier for the field.  Usually will
        be called once the field has been matched to confirm it is meets the criteria for a specific field
        name.

        :param field_node:
        :param field_criteria:
        :return:
        """

        value_specifier = field_criteria['field_value_specifier']

        if value_specifier == 'TEXT_VALUE':
            field_value = field_node.text
        elif value_specifier == 'TEXT_TAG':
            field_value = field_node.text_tag
        elif value_specifier == 'NOTE_VALUE':
            field_value = field_node.note
        elif value_specifier == 'NOTE_TAG':
            field_value = field_node.note_tag
        elif value_specifier == 'CONSTANT':
            field_value = field_criteria['field_value']
        else:
            raise ValueError(f"Unrecognised field specifier {value_specifier}")

        return field_value

    def _match_field(self, node_ancestry_record, field_ancestry_criteria):
        if node_ancestry_record.depth != len(field_ancestry_criteria):
            return False
        else:
            # Depth matches so we now need to test against provided criteria.  Each criterion corresponds to
            # a generation in the ancestry, so we need to test each generation against the appropriate criterion.
            # So we walk down the ancestry from root to current generation and check for a match.  As soon as
            # we fail to get a match, we know the node doesn't match.  If we don't fail at all generations then
            # we have a match.
            match = True

            # Create list of pairs from depth 1 to depth of node we are testing against.  Note that
            # a node list entry has ancestry starting at zero to represent the root of the outline, and
            # criteria need to start there too.
            paired_gen_and_criteria = zip(node_ancestry_record, field_ancestry_criteria)
            for pair in paired_gen_and_criteria:
                generation, gen_criteria = pair
                if not gen_criteria.matches_criteria(generation):
                    match = False

        return match


    def _override_tag_regex(self, unleashed_node):
        """
        If the specifier includes overrides for either tag or note regex, then clone the node to make a new one
        with the updated regex, otherwise just leave alone

        :param unleashed_node:
        :return:
        """
        text_regex_override = self.dns_structure['header']['tag_delimiters']['text_delimiters']
        note_regex_override = self.dns_structure['header']['tag_delimiters']['note_delimiters']

        clone = False
        if text_regex_override is not None and text_regex_override != [None, None]:
            clone = True
            text_val_to_use = text_regex_override
        else:
            text_val_to_use = unleashed_node.tag_regex_text
        if note_regex_override is not None and note_regex_override != [None, None]:
            clone = True
            note_val_to_use = note_regex_override
        else:
            note_val_to_use = unleashed_node.tag_regex_note

        if clone is True:
            return unleashed_node.clone_unleashed_node(text_tag_regex=text_val_to_use,
                                                       note_tag_regex=note_val_to_use)
        else:
            return unleashed_node


