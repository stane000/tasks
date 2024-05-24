"""
Module Docstring: Test City Summary Application

This module contains tests for a City Summary Application. It includes tests for both successful and error scenarios,
verifying the functionality and error handling of the application.

Fixtures:
    app_runner: Fixture for initializing the ApplicationTestRunner.

Test Functions:
    test_city_summary_app: Test function to verify the successful execution of the City Summary Application.
    test_city_summary_app_error_handling: Test function to verify error handling in the City Summary Application.

Constants:
    cities: List of cities to be used as test parameters in successful test cases.
    wrong_entries: List of wrong entries to be used as test parameters in error test cases.

Example Usage:
    To run the tests for successful scenarios:
        pytest.main(["-v", "-s", "-m success", __file__])
"""

import os
import pytest

from CitySummaryAppTests.tools import ApplicationTestRunner, FileChecker


@pytest.fixture(scope="module", autouse=True)
def app_runner():
    return ApplicationTestRunner()

cities = ["Zagreb", "Berlin", "london", "New York", "PARIS"]

# Test_1--------------------------------------------------------------------------------------------------------

@pytest.mark.app
@pytest.mark.success
@pytest.mark.parametrize("city", cities)
def test_city_summary_app(app_runner, city):
    """
    Test function to verify the successful execution of the City Summary Application for given city.
    Checks if summary file is created and valid!
    """
    result = app_runner.run_app(city)
    assert  "Summary created" in result, f"Summary not created, result: {result}"

    file_path = result.split(" ")[3][:-1]
    assert os.path.isfile(file_path), f"Error: file not created!"
    
    # Steps for checking validation of created file
    file_checker = FileChecker(file_path)
    file_checker.check_file_length()
    file_checker.check_if_word_in_file(city)
    file_checker.check_if_expected_temperature_in_file()

# Test_2--------------------------------------------------------------------------------------------------------

wrong_entries = ["hgff", "Python", "..", "??"]

@pytest.mark.app
@pytest.mark.error
@pytest.mark.parametrize("wrong_entire", wrong_entries)
def test_city_summary_app_error_handling(app_runner, wrong_entire):
    result = app_runner.run_app(wrong_entire)
    assert  "not exists in database" in result, f"Expected error: not exists in database, actual error: {result}"

# Example usage
if __name__ == "__main__":
    pytest.main(["-v", "-s", "-m success", os.path.abspath(__file__)])
