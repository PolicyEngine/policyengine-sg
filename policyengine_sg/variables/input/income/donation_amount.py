from policyengine_sg.model_api import *


class donation_amount(Variable):
    value_type = float
    entity = Person
    label = "Qualifying donations to approved IPCs"
    unit = SGD
    definition_period = YEAR
    default_value = 0
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "other-taxes/charities/donations-tax-deductions"
    )
