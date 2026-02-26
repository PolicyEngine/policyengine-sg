from policyengine_sg.model_api import *


class sellers_stamp_duty(Variable):
    value_type = float
    entity = Person
    label = "Seller's Stamp Duty"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/stamp-duty/"
        "for-property/selling-or-disposing-property/"
        "seller's-stamp-duty-(ssd)-for-residential"
        "-property"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.iras.stamp_duty.ssd
        price = person("property_sale_price", period)
        years = person("property_holding_years", period)
        rate = select(
            [
                years <= p.holding_period_1,
                years <= p.holding_period_2,
                years <= p.holding_period_3,
            ],
            [p.rate_1yr, p.rate_2yr, p.rate_3yr],
            default=0,
        )
        return price * rate
