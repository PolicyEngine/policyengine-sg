from policyengine_sg.model_api import *


class donation_deduction(Variable):
    value_type = float
    entity = Person
    label = "Tax deduction for qualifying donations"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "other-taxes/charities/"
        "donations-tax-deductions"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.iras.income_tax
        donations = person("donation_amount", period)
        return donations * p.donations.deduction_multiplier
