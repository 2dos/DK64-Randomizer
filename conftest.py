"""This file contains the pytest configuration for the test suite."""

import os

import pytest


def pytest_addoption(parser):
    """Add a command line option to specify the maximum acceptable failure rate for the test suite."""
    parser.addoption("--max-failure-rate", action="store", default=0.4, type=float, help="Max acceptable failure rate (default: 0.4 for 40%)")


@pytest.hookimpl(tryfirst=True)
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Log the failure rate of the test suite."""
    github_env = os.getenv("GITHUB_ENV")
    total_tests = len(terminalreporter.stats.get("passed", [])) + len(terminalreporter.stats.get("failed", []))
    failed_tests = len(terminalreporter.stats.get("failed", []))
    if total_tests > 0:
        failure_rate = failed_tests / total_tests
        max_failure_rate = config.getoption("--max-failure-rate")

        if failure_rate > max_failure_rate:
            print(f"\nTest suite failure rate ({failure_rate:.2%}) exceeds allowed limit ({max_failure_rate:.2%}).")
            if github_env:
                with open("error_status", "w") as f:
                    f.write("1")
        else:
            print(f"\nTest suite failure rate ({failure_rate:.2%}) is within the allowed limit ({max_failure_rate:.2%}).")
            # Write Success or failure to the github ENV
            if github_env:
                with open("error_status", "w") as f:
                    f.write("0")
