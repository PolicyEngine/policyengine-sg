"""
API imports for PolicyEngine Singapore model development.

This module provides convenient imports for developing variables,
parameters, and reforms for the Singapore tax-benefit system.
"""

# Import from policyengine_core
from policyengine_core.model_api import *

# Import Singapore-specific entities
from policyengine_sg.entities import (
    Person,
    TaxUnit,
    CPFUnit,
    BenefitUnit,
    Household,
)

# Currency unit
SGD = "currency-SGD"


# Common functions for Singapore calculations
def add(entity, period, variables, options=None):
    """Sum multiple variables for an entity in a period."""
    return sum(entity(variable, period, options) for variable in variables)


def subtract(entity, period, variables, options=None):
    """Subtract variables (first minus rest) for an entity in a period."""
    result = entity(variables[0], period, options)
    for variable in variables[1:]:
        result = result - entity(variable, period, options)
    return result


def multiply(entity, period, variables, options=None):
    """Multiply variables together for an entity in a period."""
    result = entity(variables[0], period, options)
    for variable in variables[1:]:
        result = result * entity(variable, period, options)
    return result
