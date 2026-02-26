from policyengine_sg.model_api import *


class gstv_medisave(Variable):
    value_type = float
    entity = Person
    label = "GST Voucher MediSave top-up"
    unit = SGD
    definition_period = YEAR
    reference = (
        "https://www.govbenefits.gov.sg/" "about-us/gst-voucher/am-i-eligible/"
    )

    def formula(person, period, parameters):
        p = parameters(period).gov.mof.gstv.medisave
        age = person("age", period)
        citizen = person("is_citizen", period)
        av = person.household("property_annual_value", period)
        n_prop = person("number_of_properties", period)
        eligible = (
            citizen
            & (age >= p.age_minimum)
            & (av <= p.av_ceiling)
            & (n_prop <= 1)
        )
        lower_av = av <= p.av_lower_threshold
        amount_lower = select(
            [age < 75, age < 85],
            [
                p.lower_av.age_65_to_74,
                p.lower_av.age_75_to_84,
            ],
            default=p.lower_av.age_85_plus,
        )
        amount_higher = select(
            [age < 75, age < 85],
            [
                p.higher_av.age_65_to_74,
                p.higher_av.age_75_to_84,
            ],
            default=p.higher_av.age_85_plus,
        )
        amount = where(lower_av, amount_lower, amount_higher)
        return where(eligible, amount, 0)
