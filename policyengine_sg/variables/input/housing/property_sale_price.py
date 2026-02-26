from policyengine_sg.model_api import *


class property_sale_price(Variable):
    value_type = float
    entity = Household
    label = "Property sale price"
    unit = SGD
    definition_period = YEAR
    default_value = 0
