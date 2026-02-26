from policyengine_sg.model_api import *


class property_holding_years(Variable):
    value_type = float
    entity = Person
    label = "Number of years property has been held (for SSD calculation)"
    definition_period = YEAR
    default_value = 99
