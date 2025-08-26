"""
Basic tests for the Singapore tax-benefit system.
"""

import pytest
from policyengine_sg import SingaporeTaxBenefitSystem


def test_system_can_be_instantiated():
    """Test that the Singapore tax-benefit system can be instantiated."""
    system = SingaporeTaxBenefitSystem()
    assert system is not None


def test_entities_are_loaded():
    """Test that all expected entities are loaded."""
    system = SingaporeTaxBenefitSystem()
    expected_entities = [
        "person",
        "tax_unit",
        "cpf_unit",
        "benefit_unit",
        "household",
    ]

    # Get the keys from entities dictionary
    entity_keys = list(system.entities.keys())
    for entity_key in expected_entities:
        assert entity_key in entity_keys
