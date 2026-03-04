from policyengine_sg.model_api import *


class total_income(Variable):
    value_type = float
    entity = Person
    label = "Total income"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "individual-income-tax/basics-of-individual"
        "-income-tax/what-is-taxable-what-is-not"
    )
    adds = [
        "employment_income",
        "self_employment_income",
        "rental_income",
        "interest_income",
        "dividend_income",
        "other_income",
    ]
