from unittest import TestCase
import os
from tempfile import TemporaryDirectory

from material_model.material_model_impl import gen_bom
from material_model.no_circular_references import validate_no_circluar_material_refs

from aac.plugins.plugin_execution import PluginExecutionStatusCode
from aac.lang.active_context_lifecycle_manager import get_active_context
from aac.io.parser import parse
from aac.plugins.validators import ValidatorFindings, ValidatorResult

from contextlib import contextmanager
from tempfile import NamedTemporaryFile, TemporaryDirectory

from valid_material_model import VALID_MATERIAL_MODEL
from circular_site_ref import CIRCULAR_SITE_REF
from circular_assembly_ref import CIRCULAR_ASSEMBLY_REF


class TestCircularReferencesValicator(TestCase):

    def test_no_circular_reference(self):

        result = _run_validator(validate_no_circluar_material_refs, VALID_MATERIAL_MODEL, "site", "My_New_Apartment")
        
        if not result.is_valid():
            raise AssertionError(f"validate_no_circular_material_refs return a validation failure for for a valid material model. isValid = {result.is_valid()} Message = {result.get_messages_as_string()}")

    def test_circular_site_reference(self):

        result = _run_validator(validate_no_circluar_material_refs, CIRCULAR_SITE_REF, "site", "My_New_Apartment")

        if result.is_valid():
            raise AssertionError(f"validate_no_circular_material_refs did not return a validation failure for circular site reference as expected.")

        expected_substring = "Circular site reference detected for My_New_Apartment"

        if expected_substring not in result.get_messages_as_string():
            raise AssertionError(f"validate_no_circular_material_refs validity was correct for circular site but error message was incorrect. Expected: {expected_substring}  Actual: {result.get_messages_as_string()}")

    def test_circular_assembly_reference(self):

        result = _run_validator(validate_no_circluar_material_refs, CIRCULAR_ASSEMBLY_REF, "assembly", "My_New_Apartment")

        if result.is_valid():
            raise AssertionError("circular_assembly_reference failed to identify a cicrular assembly reference")


        expected_substring = "Circular assembly reference detected for Seating_Area"
        if expected_substring not in result.get_messages_as_string():
            raise AssertionError(f"validate_no_circular_material_refs validity was correct for circular assembly but error message was incorrect.  Expected: {expected_substring}  Actual: {result.get_messages_as_string()}")

def _run_validator(validator_under_test, yaml_str, root_type, root_name) -> ValidatorResult:

    test_active_context = get_active_context()

    model_root_definition = None
    test_definitions = parse(yaml_str)
    test_active_context.add_definitions_to_context(test_definitions)

    for x in test_definitions:
        if x.name == root_name:
            model_root_definition = x

    target_schema_definition = test_active_context.get_definition_by_name(root_type)

    result =  validator_under_test(model_root_definition, target_schema_definition, test_active_context)

    test_active_context.clear()

    return result
