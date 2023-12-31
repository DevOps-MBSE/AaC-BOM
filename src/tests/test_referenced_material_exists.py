from unittest import TestCase

from aac.validate._validation_error import ValidationError

from material_model.referenced_material_exists import validate_referenced_materials

from test_utils import run_validator, run_core_validate

from valid_material_model import VALID_MATERIAL_MODEL
from bad_part_ref import BAD_PART_MATERIAL_REFERENCE
from bad_assembly_ref import BAD_ASSEMBLY_MATERIAL_REFERENCE
from bad_site_ref import BAD_SITE_MATERIAL_REFERENCE


class TestReferencedMaterialValidator(TestCase):

    def test_valid_model(self):

        result = run_validator(validate_referenced_materials, VALID_MATERIAL_MODEL, "site", "My_New_Apartment")

        self.assertTrue(result.is_valid(), f"validate_referenced_materials return a validation failure for for a valid material model. isValid = {result.is_valid()} Message = {result.get_messages_as_string()}")
        
    def test_core_validate_no_bad_reference(self):

        try:
            result = run_core_validate(VALID_MATERIAL_MODEL)
            self.assertTrue(result.is_valid(), f"Core validate function failed on a valid model. isValid = {result.is_valid()} Message = {result.get_messages_as_string()}")
        except ValidationError:
            self.fail(f"Unexpected validation error raised.  Received result: {result}")

    def test_core_validate_bad_part_reference(self):

        try:
            result = run_core_validate(BAD_PART_MATERIAL_REFERENCE)
            self.fail(f"Expected a validation error to be raised.  Received result: {result}")
        except ValidationError:
            pass

    def test_bad_part_reference(self):

        result = run_validator(validate_referenced_materials, BAD_PART_MATERIAL_REFERENCE, "part", "My_New_Apartment")

        self.assertFalse(result.is_valid(), "validate_referenced_materials did not return a validation failure for bad part reference as expected.")

    def test_bad_assembly_reference(self):

        result = run_validator(validate_referenced_materials, BAD_ASSEMBLY_MATERIAL_REFERENCE, "assembly", "My_New_Apartment")

        self.assertFalse(result.is_valid(), "validate_referenced_materials did not return a validation failure for bad assembly reference as expected.")

    def test_bad_site_reference(self):

        result = run_validator(validate_referenced_materials, BAD_SITE_MATERIAL_REFERENCE, "site", "My_New_Apartment")

        self.assertFalse(result.is_valid(), "validate_referenced_materials did not return a validation failure for bad site reference as expected.")
