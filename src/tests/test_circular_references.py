from unittest import TestCase

from material_model.no_circular_references import validate_no_circluar_material_refs

from test_utils import run_validator, run_core_validate

from valid_material_model import VALID_MATERIAL_MODEL
from circular_site_ref import CIRCULAR_SITE_REF
from circular_assembly_ref import CIRCULAR_ASSEMBLY_REF


class TestCircularReferencesValicator(TestCase):

    def test_no_circular_reference(self):

        result = run_validator(validate_no_circluar_material_refs, VALID_MATERIAL_MODEL, "site", "My_New_Apartment")

        self.assertTrue(result.is_valid(), f"validate_no_circular_material_refs return a validation failure for for a valid material model. isValid = {result.is_valid()} Message = {result.get_messages_as_string()}")

    def test_core_validate_no_circular_reference(self):

        result = run_core_validate(VALID_MATERIAL_MODEL)

        self.assertTrue(result.is_valid(), f"Core validate function failed on a valid model. isValid = {result.is_valid()} Message = {result.get_messages_as_string()}")

    def test_circular_site_reference(self):

        result = run_validator(validate_no_circluar_material_refs, CIRCULAR_SITE_REF, "site", "My_New_Apartment")

        self.assertFalse(result.is_valid(), "validate_no_circular_material_refs did not return a validation failure for circular site reference as expected.")

        expected_substring = "Circular site reference detected for My_New_Apartment"

        if expected_substring not in result.get_messages_as_string():
            raise AssertionError(f"validate_no_circular_material_refs validity was correct for circular site but error message was incorrect. Expected: {expected_substring}  Actual: {result.get_messages_as_string()}")
        
    # def test_core_validate_circular_site_reference(self):

    #     result = run_core_validate(CIRCULAR_SITE_REF)

    #     self.assertFalse(result.is_valid(), "core validate did not return a validation failure for circular site reference as expected.")

    def test_circular_assembly_reference(self):

        result = run_validator(validate_no_circluar_material_refs, CIRCULAR_ASSEMBLY_REF, "assembly", "My_New_Apartment")

        self.assertFalse(result.is_valid(), "circular_assembly_reference failed to identify a cicrular assembly reference")

        expected_substring = "Circular assembly reference detected for Seating_Area"
        if expected_substring not in result.get_messages_as_string():
            raise AssertionError(f"validate_no_circular_material_refs validity was correct for circular assembly but error message was incorrect.  Expected: {expected_substring}  Actual: {result.get_messages_as_string()}")
