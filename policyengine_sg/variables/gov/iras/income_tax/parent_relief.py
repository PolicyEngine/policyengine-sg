from policyengine_sg.model_api import *


class parent_relief(Variable):
    value_type = float
    entity = Person
    label = "Parent relief"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "individual-income-tax/basics-of-individual"
        "-income-tax/tax-reliefs-rebates-and-"
        "deductions/tax-reliefs/parent-relief-"
        "parent-relief-(disability)"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.iras.income_tax.reliefs.parent
        n_living = person("number_of_dependant_parents", period)
        n_not = person(
            "number_of_dependant_parents_not_living",
            period,
        )
        n_dis_living = person("number_of_disabled_parents", period)
        n_dis_not = person(
            "number_of_disabled_parents_not_living",
            period,
        )
        return (
            n_living * p.living_together
            + n_not * p.not_living_together
            + n_dis_living * p.disability_living_together
            + n_dis_not * p.disability_not_living_together
        )
