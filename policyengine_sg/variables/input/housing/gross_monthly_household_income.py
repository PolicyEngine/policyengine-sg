from policyengine_sg.model_api import *


class gross_monthly_household_income(Variable):
    value_type = float
    entity = Person
    label = "Gross monthly household income"
    unit = SGD
    definition_period = YEAR
    default_value = 0
