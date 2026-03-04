from policyengine_sg.model_api import *


class household_income_per_capita(Variable):
    value_type = float
    entity = Person
    label = "Monthly household income per capita" " for benefit eligibility"
    unit = SGD
    definition_period = YEAR
    default_value = 0
