from policyengine_sg.model_api import *


class is_resident(Variable):
    value_type = bool
    entity = Person
    label = "Whether the person is a tax resident"
    definition_period = YEAR
    default_value = True
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "individual-income-tax/basics-of-individual"
        "-income-tax/tax-residency-and-tax-rates/"
        "individual-income-tax-rates"
    )
