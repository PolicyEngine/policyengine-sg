from policyengine_sg.model_api import *


class childcare_subsidy(Variable):
    value_type = float
    entity = Person
    label = "Annual childcare subsidy (basic + additional)"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.ecda.gov.sg/parents/"
        "preschool-subsidies/"
        "infant-and-childcare-subsidy-scheme/overview"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.ecda.childcare_subsidy
        citizen = person("is_citizen", period)
        working = person("is_working_mother", period)
        n_cc = person("number_of_children_in_childcare", period)
        n_ic = person("number_of_children_in_infant_care", period)
        ghi = person("gross_monthly_household_income", period)
        basic_cc = where(working, p.basic_childcare, 0)
        basic_ic = where(working, p.basic_infant_care, 0)
        additional = p.additional.calc(ghi)
        monthly = n_cc * (basic_cc + additional) + n_ic * (
            basic_ic + additional
        )
        return where(citizen, monthly * 12, 0)
