from policyengine_sg.model_api import *
from policyengine_sg.variables.input.housing.hdb_flat_type import (
    HDBFlatType,
)


class gstv_scc_rebate(Variable):
    value_type = float
    entity = Household
    label = "GST Voucher S&CC rebate"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.govbenefits.gov.sg/" "about-us/gst-voucher/am-i-eligible/"
    )

    def formula(household, period, parameters):
        p = parameters(period).gov.mof.gstv.scc
        flat_type = household("hdb_flat_type", period)
        is_hdb = flat_type != HDBFlatType.NON_HDB
        months = select(
            [
                (flat_type == HDBFlatType.ONE_ROOM)
                | (flat_type == HDBFlatType.TWO_ROOM),
                flat_type == HDBFlatType.THREE_ROOM,
                flat_type == HDBFlatType.FOUR_ROOM,
                flat_type == HDBFlatType.FIVE_ROOM,
                flat_type == HDBFlatType.EXECUTIVE,
            ],
            [
                p.months.one_two_room,
                p.months.three_room,
                p.months.four_room,
                p.months.five_room,
                p.months.executive,
            ],
            default=0,
        )
        scc = household("monthly_scc_charge", period)
        return where(is_hdb, months * scc, 0)
