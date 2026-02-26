from policyengine_sg.model_api import *


class property_tax(Variable):
    value_type = float
    entity = Household
    label = "Property tax"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "property-tax/property-owners/"
        "property-tax-rates"
    )

    def formula(household, period, parameters):
        p = parameters(period).gov.iras.property_tax
        av = household("property_annual_value", period)
        is_oo = household("is_owner_occupied", period)
        oo_tax = p.owner_occupied.rates.calc(av)
        noo_tax = p.non_owner_occupied.rates.calc(av)
        return where(is_oo, oo_tax, noo_tax)
