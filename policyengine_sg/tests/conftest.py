"""
Pytest configuration for PolicyEngine Singapore tests.
"""

import pytest
from policyengine_sg.system import SingaporeTaxBenefitSystem


@pytest.fixture(scope="session")
def system():
    """Create a Singapore tax-benefit system for testing."""
    return SingaporeTaxBenefitSystem()
