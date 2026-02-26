from policyengine_sg.model_api import *


class property_annual_value(Variable):
    value_type = float
    entity = Household
    label = "Annual value of property"
    unit = SGD
    definition_period = YEAR
    default_value = 0
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "property-tax/property-owners/"
        "property-tax-rates"
    )
