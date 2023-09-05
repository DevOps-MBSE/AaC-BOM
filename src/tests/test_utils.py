from aac.lang.active_context_lifecycle_manager import get_active_context
from aac.io.parser import parse
from aac.plugins.validators import ValidatorFindings, ValidatorResult

def run_validator(validator_under_test, yaml_str, root_type, root_name) -> ValidatorResult:

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