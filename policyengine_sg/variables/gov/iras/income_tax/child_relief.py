from policyengine_sg.model_api import *


class child_relief(Variable):
    value_type = float
    entity = Person
    label = "Qualifying child relief"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "individual-income-tax/basics-of-individual"
        "-income-tax/tax-reliefs-rebates-and-"
        "deductions/tax-reliefs/qualifying-child-"
        "relief-(qcr)-child-relief-(disability)"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.iras.income_tax.reliefs.child
        n_children = person("number_of_children", period)
        n_disabled = person(
            "number_of_children_with_disability",
            period,
        )
        normal = (n_children - n_disabled) * (p.qualifying_amount)
        disabled = n_disabled * p.disability_amount
        return normal + disabled
