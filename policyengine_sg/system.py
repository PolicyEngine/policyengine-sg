"""
Singapore Tax-Benefit System implementation.
"""

import os
from policyengine_core.taxbenefitsystems import TaxBenefitSystem
from policyengine_sg.entities import entities

# Import all variables
from policyengine_sg.variables.input.demographics.age import age
from policyengine_sg.variables.input.income.employment_income import (
    employment_income,
)
from policyengine_sg.variables.gov.cpf.cpf_eligible_age import cpf_eligible_age
from policyengine_sg.variables.gov.cpf.cpf_ordinary_wage import (
    cpf_ordinary_wage,
)
from policyengine_sg.variables.gov.cpf.cpf_additional_wage import (
    cpf_additional_wage,
)
from policyengine_sg.variables.gov.cpf.cpf_employee_contribution import (
    cpf_employee_contribution,
)
from policyengine_sg.variables.gov.cpf.cpf_employer_contribution import (
    cpf_employer_contribution,
)
from policyengine_sg.variables.gov.cpf.cpf_total_contribution import (
    cpf_total_contribution,
)


COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))


class SingaporeTaxBenefitSystem(TaxBenefitSystem):
    """Singapore tax-benefit system."""

    def __init__(self):
        """Initialize the Singapore tax-benefit system."""
        super().__init__(entities)

        # Load parameters
        self.load_parameters(os.path.join(COUNTRY_DIR, "parameters"))

        # Add variables manually
        self.add_variables(
            age,
            employment_income,
            cpf_eligible_age,
            cpf_ordinary_wage,
            cpf_additional_wage,
            cpf_employee_contribution,
            cpf_employer_contribution,
            cpf_total_contribution,
        )
