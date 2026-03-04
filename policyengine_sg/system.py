"""
Singapore Tax-Benefit System implementation.
"""

import os
from policyengine_core.taxbenefitsystems import TaxBenefitSystem
from policyengine_sg.entities import entities

COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))


class SingaporeTaxBenefitSystem(TaxBenefitSystem):
    """Singapore tax-benefit system."""

    def __init__(self):
        """Initialize the Singapore tax-benefit system."""
        super().__init__(entities)

        # Load parameters
        self.load_parameters(os.path.join(COUNTRY_DIR, "parameters"))

        # Load variables
        self.add_variables_from_directory(
            os.path.join(COUNTRY_DIR, "variables")
        )
