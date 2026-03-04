from policyengine_sg.model_api import *


class chargeable_income(Variable):
    value_type = float
    entity = Person
    label = "Chargeable income"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "individual-income-tax/basics-of-individual"
        "-income-tax/taxable-income"
    )

    def formula(person, period, parameters):
        total = person("total_income", period)
        donations = person("donation_deduction", period)
        reliefs = person("total_personal_reliefs", period)
        return max_(total - donations - reliefs, 0)
