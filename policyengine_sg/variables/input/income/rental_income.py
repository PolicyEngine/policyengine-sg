from policyengine_sg.model_api import *


class rental_income(Variable):
    value_type = float
    entity = Person
    label = "Rental income"
    unit = SGD
    definition_period = YEAR
    default_value = 0
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "individual-income-tax/basics-of-individual"
        "-income-tax/what-is-taxable-what-is-not/"
        "income-from-property-rented-out"
    )
