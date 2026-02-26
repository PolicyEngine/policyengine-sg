from policyengine_sg.model_api import *


class comcare_lta(Variable):
    value_type = float
    entity = BenefitUnit
    label = "ComCare Long-Term Assistance" " annual payment"
    unit = SGD
    definition_period = YEAR
    reference = "https://www.msf.gov.sg/what-we-do/comcare"

    def formula(benefit_unit, period, parameters):
        p = parameters(period).gov.msf.comcare.lta
        n_members = benefit_unit.nb_persons()
        capped_size = min_(n_members, p.max_household_size)
        monthly = p.amount.calc(capped_size)
        eligible = benefit_unit.any(
            benefit_unit.members("comcare_eligible", period)
        )
        return where(eligible, monthly * 12, 0)
