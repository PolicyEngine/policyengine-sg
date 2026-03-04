from policyengine_sg.model_api import *


class cdc_vouchers(Variable):
    value_type = float
    entity = Household
    label = "CDC Vouchers"
    unit = SGD
    definition_period = YEAR
    reference = "https://vouchers.cdc.gov.sg/about/"

    def formula(household, period, parameters):
        p = parameters(period).gov.mof.cdc_vouchers
        has_citizen = household.any(household.members("is_citizen", period))
        return where(has_citizen, p.amount, 0)
