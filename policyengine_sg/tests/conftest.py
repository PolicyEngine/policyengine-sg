"""
Pytest configuration for PolicyEngine Singapore tests.
"""

import pytest
from policyengine_sg.system import SingaporeTaxBenefitSystem
from policyengine_core.tools.test_runner import OpenFiscaPlugin


@pytest.fixture(scope="session")
def system():
    """Create a Singapore tax-benefit system for testing."""
    return SingaporeTaxBenefitSystem()


def pytest_collect_file(parent, file_path):
    """Collect YAML test files for PolicyEngine."""
    if file_path.suffix in [".yaml", ".yml"]:
        tax_benefit_system = SingaporeTaxBenefitSystem()
        plugin = OpenFiscaPlugin(tax_benefit_system, {})
        return plugin.pytest_collect_file(parent, file_path)
