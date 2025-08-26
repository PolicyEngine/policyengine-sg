"""
CPF eligibility based on age for Singapore CPF system.
"""

from policyengine_sg.model_api import *


class cpf_eligible_age(Variable):
    value_type = bool
    entity = Person
    label = "CPF eligible by age"
    definition_period = YEAR
    default_value = False
    reference = "https://www.cpf.gov.sg/member/faq/growing-your-savings/saving-for-my-retirement/what-is-the-minimum-age-to-contribute-to-cpf"
    documentation = """
    Determines if a person is eligible for CPF contributions based on age.
    
    CPF contributions are required for:
    - Singapore Citizens and Permanent Residents
    - From age 16 until the last day of the month in which they turn 70
    
    Based on CPF Act Section 7.
    """

    def formula(person, period, parameters):
        age = person("age", period)
        
        # CPF eligible from age 16 to 70 (inclusive)
        # Age changes affect contributions from first day of month after birthday
        return (age >= 16) & (age <= 70)


def test_cpf_eligible_age():
    """Test CPF age eligibility rules."""
    from policyengine_sg import Microsimulation
    
    # Test case 1: Under 16 - not eligible
    sim = Microsimulation()
    sim.set_input("age", 2025, [15])
    result = sim.calculate("cpf_eligible_age", 2025)
    assert result[0] == False
    
    # Test case 2: Age 16 - eligible
    sim.set_input("age", 2025, [16])
    result = sim.calculate("cpf_eligible_age", 2025)
    assert result[0] == True
    
    # Test case 3: Working age - eligible
    sim.set_input("age", 2025, [35])
    result = sim.calculate("cpf_eligible_age", 2025)
    assert result[0] == True
    
    # Test case 4: Age 70 - still eligible
    sim.set_input("age", 2025, [70])
    result = sim.calculate("cpf_eligible_age", 2025)
    assert result[0] == True
    
    # Test case 5: Over 70 - not eligible
    sim.set_input("age", 2025, [71])
    result = sim.calculate("cpf_eligible_age", 2025)
    assert result[0] == False