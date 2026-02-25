from policyengine_sg.model_api import *
from policyengine_sg.variables.input.housing.hdb_flat_type import (
    HDBFlatType,
)


class gstv_u_save(Variable):
    value_type = float
    entity = Household
    label = "GST Voucher U-Save annual rebate"
    unit = SGD
    definition_period = YEAR
    reference = "https://www.govbenefits.gov.sg/" "about-us/gst-voucher/"

    def formula(household, period, parameters):
        p = parameters(period).gov.mof.gstv.u_save
        flat_type = household("hdb_flat_type", period)
        quarterly = select(
            [
                (flat_type == HDBFlatType.ONE_ROOM)
                | (flat_type == HDBFlatType.TWO_ROOM),
                flat_type == HDBFlatType.THREE_ROOM,
                flat_type == HDBFlatType.FOUR_ROOM,
                flat_type == HDBFlatType.FIVE_ROOM,
                flat_type == HDBFlatType.EXECUTIVE,
            ],
            [
                p.quarterly.one_two_room,
                p.quarterly.three_room,
                p.quarterly.four_room,
                p.quarterly.five_room,
                p.quarterly.executive,
            ],
            default=0,
        )
        return quarterly * p.quarters_per_year
