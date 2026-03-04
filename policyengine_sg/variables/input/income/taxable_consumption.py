from policyengine_sg.model_api import *


class taxable_consumption(Variable):
    value_type = float
    entity = Household
    label = "Taxable goods and services consumption"
    unit = SGD
    definition_period = YEAR
    default_value = 0
