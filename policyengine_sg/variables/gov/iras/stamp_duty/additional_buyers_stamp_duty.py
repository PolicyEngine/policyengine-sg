from policyengine_sg.model_api import *
from policyengine_sg.variables.input.housing.buyer_profile import (
    BuyerProfile,
)


class additional_buyers_stamp_duty(Variable):
    value_type = float
    entity = Household
    label = "Additional buyer's stamp duty" " on property purchase"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/stamp-duty/"
        "for-property/buying-or-acquiring-property/"
        "additional-buyer's-stamp-duty-(absd)"
    )

    def formula(household, period, parameters):
        p = parameters(period).gov.iras.stamp_duty.absd
        price = household("property_purchase_price", period)
        profile = household("buyer_profile", period)
        rate = select(
            [
                profile == BuyerProfile.CITIZEN_FIRST,
                profile == BuyerProfile.CITIZEN_SECOND,
                profile == BuyerProfile.CITIZEN_THIRD_AND_SUBSEQUENT,
                profile == BuyerProfile.PR_FIRST,
                profile == BuyerProfile.PR_SECOND,
                profile == BuyerProfile.PR_THIRD_AND_SUBSEQUENT,
                profile == BuyerProfile.FOREIGNER,
            ],
            [
                p.citizen_first,
                p.citizen_second,
                p.citizen_third_and_subsequent,
                p.pr_first,
                p.pr_second,
                p.pr_third_and_subsequent,
                p.foreigner,
            ],
            default=p.foreigner,
        )
        return price * rate
