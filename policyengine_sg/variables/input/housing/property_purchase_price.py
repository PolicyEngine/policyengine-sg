from policyengine_sg.model_api import *


class property_purchase_price(Variable):
    value_type = float
    entity = Household
    label = "Property purchase price or market value"
    unit = SGD
    definition_period = YEAR
    default_value = 0
