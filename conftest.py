"""This file contains the pytest configuration for the test suite."""

import pytest


def pytest_addoption(parser):
    """Add a command line option to specify the maximum acceptable failure rate for the test suite."""
    parser.addoption("--max-failure-rate", action="store", default=0.4, type=float, help="Max acceptable failure rate (default: 0.4 for 40%)")


@pytest.hookimpl(tryfirst=True)
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Check the failure rate of the test suite and fail if it exceeds the maximum acceptable rate."""
    total_tests = terminalreporter.stats.get("passed", 0) + terminalreporter.stats.get("failed", 0)
    failed_tests = terminalreporter.stats.get("failed", 0)
    total_tests = len(total_tests)
    failed_tests = len(failed_tests)
    if total_tests > 0:
        failure_rate = failed_tests / total_tests
        max_failure_rate = config.getoption("--max-failure-rate")

        if failure_rate > max_failure_rate:
            print(f"\nTest suite failure rate ({failure_rate:.2%}) exceeds allowed limit ({max_failure_rate:.2%}).")
            exitstatus |= 1
        else:
            print(f"\nTest suite failure rate ({failure_rate:.2%}) is within the allowed limit ({max_failure_rate:.2%}).")
