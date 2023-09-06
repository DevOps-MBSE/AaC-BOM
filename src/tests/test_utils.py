import os
from contextlib import contextmanager
from tempfile import NamedTemporaryFile, TemporaryDirectory

from aac.lang.active_context_lifecycle_manager import get_active_context
from aac.io.parser import parse
from aac.plugins.validators import ValidatorResult


def run_validator(validator_under_test, yaml_str, root_type, root_name) -> ValidatorResult:

    test_active_context = get_active_context()

    model_root_definition = None
    test_definitions = parse(yaml_str)
    test_active_context.add_definitions_to_context(test_definitions)

    for x in test_definitions:
        if x.name == root_name:
            model_root_definition = x

    target_schema_definition = test_active_context.get_definition_by_name(root_type)

    result = validator_under_test(model_root_definition, target_schema_definition, test_active_context)

    test_active_context.clear()

    return result


# Test helper functions
@contextmanager
def temporary_test_file(content: str, **extra_file_attrs):
    """Create a temporary file containing content for testing.

    Arguments:
        content (str): A string to use as the contents of the file.
        extra_file_attrs (dict): Extra file attributes that will be used when creating the test
                                 file. These should be valid parameters to NamedTemporaryFile.
                                 (optional)
            Extra file attributes:
                * mode (default value is "w")
                * buffering (default value is - 1)
                * encoding (default value is None)
                * newline (default value is None)
                * suffix (default value is None)
                * prefix (default value is None)
                * dir (default value is `TemporaryDirectory()`)

    Yields:
        The temporary test file containing the specified contents.
    """
    with TemporaryDirectory() as temp_dir:
        new_directory = extra_file_attrs.get("dir") or temp_dir
        mode = extra_file_attrs.get("mode") or "w"
        extra_file_attrs |= {"dir": new_directory, "mode": mode}
        with new_working_dir(new_directory), NamedTemporaryFile(**extra_file_attrs) as file:
            file.write(content)
            file.seek(0)

            yield file


@contextmanager
def new_working_dir(directory):
    """Change directories to execute some code, then change back.

    Args:
        directory: The new working directory to switch to.

    Returns:
        The new working directory.

    Example Usage:
        from os import getcwd
        from tempfile import TemporaryDirectory

        print(getcwd())
        with TemporaryDirectory() as tmpdir, new_working_dir(tmpdir):
            print(getcwd())
        print(getcwd())
    """
    current_dir = os.getcwd()
    try:
        os.chdir(directory)
        yield os.getcwd()
        os.chdir(current_dir)
    except Exception as e:
        os.chdir(current_dir)
        raise e
