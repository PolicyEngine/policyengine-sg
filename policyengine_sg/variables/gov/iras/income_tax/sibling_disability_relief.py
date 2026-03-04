from policyengine_sg.model_api import *


class sibling_disability_relief(Variable):
    value_type = float
    entity = Person
    label = "Handicapped sibling relief"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "individual-income-tax/basics-of-individual"
        "-income-tax/tax-reliefs-rebates-and-"
        "deductions/tax-reliefs/"
        "sibling-relief-(disability)"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.iras.income_tax.reliefs.sibling_disability
        n_siblings = person("number_of_disabled_siblings", period)
        return n_siblings * p.amount
