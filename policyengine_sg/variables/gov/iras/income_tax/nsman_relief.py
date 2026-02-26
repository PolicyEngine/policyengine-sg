from policyengine_sg.model_api import *
from policyengine_sg.variables.input.demographics.nsman_status import (
    NsmanStatus,
)


class nsman_relief(Variable):
    value_type = float
    entity = Person
    label = "NSman relief"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.iras.gov.sg/taxes/"
        "individual-income-tax/basics-of-individual"
        "-income-tax/tax-reliefs-rebates-and-"
        "deductions/tax-reliefs/nsman-relief-"
        "(self-wife-and-parent)"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.iras.income_tax.reliefs.nsman
        status = person("nsman_status", period)
        self_amount = select(
            [
                status == NsmanStatus.ACTIVE,
                status == NsmanStatus.NON_ACTIVE,
                status == NsmanStatus.KEY_APPOINTMENT_ACTIVE,
                status == NsmanStatus.KEY_APPOINTMENT_NON_ACTIVE,
            ],
            [
                p.active,
                p.non_active,
                p.key_appointment,
                p.key_appointment_non_active,
            ],
            default=0,
        )
        wife = person("is_wife_of_nsman", period)
        parent = person("is_parent_of_nsman", period)
        wife_amount = where(wife, p.wife, 0)
        parent_amount = where(parent, p.parent, 0)
        # Mutual exclusivity: cannot combine self + wife/parent
        family_amount = wife_amount + parent_amount
        return max_(self_amount, family_amount)
