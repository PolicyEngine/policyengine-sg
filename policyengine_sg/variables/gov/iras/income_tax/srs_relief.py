from policyengine_sg.model_api import *


class srs_relief(Variable):
    value_type = float
    entity = Person
    label = "SRS contribution relief"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "individual-income-tax/basics-of-individual"
        "-income-tax/special-tax-schemes/"
        "srs-contributions"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.iras.income_tax.reliefs.srs
        contribution = person("srs_contribution", period)
        is_citizen = person("is_citizen", period)
        is_pr = person("is_pr", period)
        cap = where(
            is_citizen | is_pr,
            p.citizen_pr_amount,
            p.foreigner_amount,
        )
        return min_(contribution, cap)
