from policyengine_sg.model_api import *


class buyers_stamp_duty(Variable):
    value_type = float
    entity = Household
    label = "Buyer's stamp duty on property purchase"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/stamp-duty/"
        "for-property/buying-or-acquiring-property/"
        "buyer's-stamp-duty-(bsd)"
    )

    def formula(household, period, parameters):
        p = parameters(period).gov.iras.stamp_duty.bsd
        price = household("property_purchase_price", period)
        return p.rates.calc(price)
