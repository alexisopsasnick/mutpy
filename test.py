import mutate as mu
import ast as a

import main as m
from redbaron import RedBaron
import runner as r

TEST_DIR = 'test_data/pytest_examples/'
TEST_FILES = list(map((lambda x: TEST_DIR + x), ['test_some_pass.py', 'test_all_pass.py', 'test_all_fail.py', 'test_empty']))

def test_str_to_ast():
    valid_python = "2 + 2"
    observed = mu.str_to_ast(valid_python)
    assert isinstance(observed, a.AST)

def test_ast_to_str():
    # TODO: flaky test! we don't want to test for exact equality, but instead for same result of execution
    valid_python = "(2 + 2)"
    some_ast = a.parse(valid_python)
    observed = mu.ast_to_str(some_ast)
    assert valid_python == observed

def test_validate_ast():
    valid_python = "(2 + 2)"
    some_ast = a.parse(valid_python)
    result = mu.validate_ast(some_ast)
    assert result

def test_verify_mutation():
    program_a_str = "1 + 1"
    program_b_str = "2 + 2"
    program_a_ast = mu.str_to_ast(program_a_str)
    program_b_ast = mu.str_to_ast(program_b_str)
    assert mu.verify_mutation(program_a_ast, program_b_ast)

def test_count_nodes():
    valid_python = "2+2;3+3;x=2"
    EXPECTED_N_NODES = 3
    program_ast = a.parse(valid_python)
    observed_n_nodes = mu.count_nodes(program_ast)
    assert EXPECTED_N_NODES == observed_n_nodes

def test_pytest_result():
    ''' result of capturing the result of running a test in code is a string '''
    test_file = TEST_FILES[0]
    observed_result = r.pytest_result(test_file)
    assert isinstance(observed_result, str)

def test_find_total():
    ''' successfully parse result of running tests to yield int representation of total tests for mixed result file '''
    test_file = TEST_FILES[0]
    pytest_result = r.pytest_result(test_file)
    EXPECTED_TOTAL = 2
    observed_total = r.find_total(pytest_result)
    assert EXPECTED_TOTAL == observed_total

def test_find_passed():
    ''' successfully parse result of running tests to yield int representation of passed tests for mixed result file '''
    test_file = TEST_FILES[0]
    pytest_result = r.pytest_result(test_file)
    EXPECTED_PASSED = 1
    observed_passed = r.find_passed(pytest_result)
    assert EXPECTED_PASSED == observed_passed

def test_find_failed():
    ''' successfully parse result of running tests to yield int representation of failed tests for mixed result file '''
    test_file = TEST_FILES[0]
    pytest_result = r.pytest_result(test_file)
    EXPECTED_FAILED = 1
    observed_failed = r.find_failed(pytest_result)
    assert EXPECTED_FAILED == observed_failed

def test_find_time():
    ''' successfully parse result of running tests to yield int representation of passed tests for mixed result file '''
    test_file = TEST_FILES[0]
    pytest_result = r.pytest_result(test_file)
    observed_time = r.find_time(pytest_result)
    assert isinstance(observed_time, float)

def test_parse_pytest_result_mixed():
    ''' end-to-end test of parsing test result to dict for test file of mixed results '''
    test_file = TEST_FILES[0]
    EXPECTED_PASSED = 1
    EXPECTED_FAILED = 1
    EXPECTED_TOTAL = 2
    actual = r.parse_pytest_result(test_file)
    actual_passed = actual["passed"]
    actual_failed = actual["failed"]
    actual_total = actual["total"]
    time = actual["time"]
    assert actual_passed == EXPECTED_PASSED and actual_failed == EXPECTED_FAILED and isinstance(time, float) and actual_total == EXPECTED_TOTAL

def test_parse_pytest_result_passing():
    ''' end-to-end test of parsing test result to dict for test file of uniform passing results '''
    test_file = TEST_FILES[1]
    EXPECTED_PASSED = 2
    EXPECTED_FAILED = None
    EXPECTED_TOTAL = 2
    actual = r.parse_pytest_result(test_file)
    actual_passed = actual["passed"]
    actual_failed = actual["failed"]
    actual_total = actual["total"]
    time = actual["time"]
    assert actual_passed == EXPECTED_PASSED and actual_failed == EXPECTED_FAILED and isinstance(time, float) and actual_total == EXPECTED_TOTAL

def test_parse_pytest_result_failing():
    ''' end-to-end test of parsing test result to dict for test file of uniform failing results '''
    test_file = TEST_FILES[2]
    EXPECTED_PASSED = None
    EXPECTED_FAILED = 2
    EXPECTED_TOTAL = 2
    actual = r.parse_pytest_result(test_file)
    actual_passed = actual["passed"]
    actual_failed = actual["failed"]
    actual_total = actual["total"]
    time = actual["time"]
    assert actual_passed == EXPECTED_PASSED and actual_failed == EXPECTED_FAILED and isinstance(time, float) and actual_total == EXPECTED_TOTAL

def test_parse_pytest_result_empty():
    ''' end-to-end test of parsing test result to dict for an empty test file '''
    test_file = TEST_FILES[3]
    EXPECTED_PASSED = None
    EXPECTED_FAILED = None
    EXPECTED_TOTAL = None
    actual = r.parse_pytest_result(test_file)
    actual_passed = actual["passed"]
    actual_failed = actual["failed"]
    actual_total = actual["total"]
    time = actual["time"]
    assert actual_passed == EXPECTED_PASSED and actual_failed == EXPECTED_FAILED and isinstance(time, float) and actual_total == EXPECTED_TOTAL
