from policyengine_sg.model_api import *


class scfa(Variable):
    value_type = float
    entity = Person
    label = "Student Care Fee Assistance (annual)"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.msf.gov.sg/what-we-do/"
        "student-care/for-parents/"
        "student-care-fee-assistance"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.msf.scfa
        citizen = person("is_citizen", period)
        n_sc = person(
            "number_of_children_in_student_care",
            period,
        )
        ghi = person("gross_monthly_household_income", period)
        monthly = n_sc * p.subsidy.calc(ghi)
        return where(citizen, monthly * 12, 0)
