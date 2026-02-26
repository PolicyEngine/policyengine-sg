from policyengine_sg.model_api import *


class total_stamp_duty(Variable):
    value_type = float
    entity = Household
    label = "Total stamp duty on property purchase"
    unit = SGD
    definition_period = YEAR
    reference = "https://www.iras.gov.sg/taxes/stamp-duty/for-property/buying-or-acquiring-property"
    adds = [
        "buyers_stamp_duty",
        "additional_buyers_stamp_duty",
    ]
