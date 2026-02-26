from policyengine_sg.model_api import *


class gst(Variable):
    value_type = float
    entity = Household
    label = "Goods and Services Tax payable"
    unit = SGD
    definition_period = YEAR
    reference = "https://www.iras.gov.sg/taxes/" "goods-services-tax-(gst)"

    def formula(household, period, parameters):
        p = parameters(period).gov.iras.gst
        consumption = household("taxable_consumption", period)
        return consumption * p.rate
