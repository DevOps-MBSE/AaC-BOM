
from unittest import TestCase
from tempfile import TemporaryDirectory

from material_model.material_model_impl import gen_bom

from aac.plugins.plugin_execution import PluginExecutionStatusCode

from test_utils import temporary_test_file, new_working_dir

from valid_material_model import VALID_MATERIAL_MODEL


class TestMaterialModel(TestCase):

    def test_gen_bom(self):
        with (
            TemporaryDirectory() as temp_dir,
            temporary_test_file(VALID_MATERIAL_MODEL, dir=temp_dir) as temp_arch_file,
            new_working_dir(temp_dir),
        ):

            result = gen_bom(temp_arch_file.name, temp_dir)
            self.assertEqual(result.status_code, PluginExecutionStatusCode.SUCCESS)

            # assert BOM was actually written
            with open("bom.csv") as bom_csv_file:

                bom_lines = bom_csv_file.readlines()

                self.assertEqual(len(bom_lines), 20, "Incorrect BOM csv line count")  # There should be 1 header + 19 data lines

                # Assert csv contents are present
                self.assertIn("name,make,model,description,quantity,unit_cost,total_cost,need_date,location\n", bom_lines, "Header not presentin BOM csv")
                
                self.assertIn(
                    "My_New_Apartment / Kitchen / Appliances / Blender,Grind House,Liquificationinator 1000,7 setting industrial strength blender with pulse,1,99.99,99.99,,Crystal Terrace Apartments Unit 1234 / The room with the sink and the stove\n",
                    bom_lines, "Expected line for blender not found in BOM csv")
