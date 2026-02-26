from policyengine_sg.model_api import *


class kifas(Variable):
    value_type = float
    entity = Person
    label = "KiFAS kindergarten fee assistance (annual)"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.ecda.gov.sg/parents/"
        "preschool-subsidies/"
        "kindergarten-fee-assistance-scheme-(kifas)"
        "/overview"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.ecda.kifas
        citizen = person("is_citizen", period)
        n_k = person(
            "number_of_children_in_kindergarten",
            period,
        )
        ghi = person("gross_monthly_household_income", period)
        monthly = n_k * p.subsidy.calc(ghi)
        return where(citizen, monthly * 12, 0)
