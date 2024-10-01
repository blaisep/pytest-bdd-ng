import re
import shutil
import string
from operator import attrgetter, itemgetter
from pathlib import Path
from typing import TYPE_CHECKING

from pytest_bdd import given, step
from pytest_bdd.compatibility.pytest import assert_outcomes
from pytest_bdd.testing_utils import data_table_to_dicts
from pytest_bdd.utils import compose

if TYPE_CHECKING:  # pragma: no cover
    from pytest_bdd.compatibility.pytest import Testdir


@given(re.compile('File "(?P<name>\\w+)(?P<extension>\\.\\w+)" with (?P<extra_opts>.*|\\s)content:'))
def write_file_with_extras(name, extension, testdir, step, request, extra_opts, tmp_path):
    content = step.doc_string.content
    is_fixture_templated = "fixture templated" in extra_opts
    if is_fixture_templated:
        template_fields = [field_name for _, field_name, _, _ in string.Formatter().parse(content) if field_name]

        format_options = dict(
            map(lambda fixture_name: (fixture_name, str(request.getfixturevalue(fixture_name))), template_fields)
        )
    makefile_arg = {name: str(content).format_map(format_options) if is_fixture_templated else content}
    testdir.makefile(extension, **makefile_arg)


@given(
    re.compile('File "(?P<name>\\w+)(?P<extension>\\.\\w+)" in the temporary path with content:'),
    target_fixture="bypass_tmp_path",
)
def write_file(name, extension, tmp_path: Path, step):
    content = step.doc_string.content
    (tmp_path / f"{name}{extension}").write_text(content)
    yield tmp_path


@given(re.compile("Set pytest.ini content to:"))
def _(testdir, step):
    content = step.doc_string.content
    testdir.makeini(content)


@step("run pytest", target_fixture="pytest_result")
def run_pytest(testdir, step):
    options_dict = data_table_to_dicts(step.data_table)
    testrunner = (
        testdir.runpytest_inprocess if options_dict.get("subprocess", [False])[0] == "true" else testdir.runpytest
    )

    outcome = testrunner(*options_dict.get("cli_args", []))

    yield outcome


@step("pytest outcome must contain tests with statuses:")
def check_pytest_test_statuses(pytest_result, step):
    outcomes_kwargs = map(attrgetter("value"), step.data_table.rows[0].cells)
    outcomes_kwargs_values = map(compose(int, attrgetter("value")), step.data_table.rows[1].cells)
    outcome_result = dict(zip(outcomes_kwargs, outcomes_kwargs_values))

    assert_outcomes(pytest_result, **outcome_result)


@step("pytest outcome must match lines:")
def check_pytest_stdout_lines(pytest_result, step):
    lines = list(map(compose(attrgetter("value"), itemgetter(0)), map(attrgetter("cells"), step.data_table.rows)))

    pytest_result.stdout.fnmatch_lines(lines)


@given(re.compile(r"Copy path from \"(?P<initial_path>(\w|\\|.)+)\" to test path \"(?P<final_path>(\w|\\|.)+)\""))
def copy_path(request, testdir: "Testdir", initial_path, final_path, step):
    full_initial_path = (Path(request.config.rootdir) / Path(initial_path).as_posix()).resolve(strict=True)
    full_final_path = Path(testdir.tmpdir) / Path(final_path).as_posix()
    if full_initial_path.is_file():
        full_final_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(full_initial_path, full_final_path)
    else:
        shutil.copytree(full_initial_path, full_final_path, dirs_exist_ok=True)
