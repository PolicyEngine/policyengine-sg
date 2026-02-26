from policyengine_sg.model_api import *


class gstv_cash(Variable):
    value_type = float
    entity = Person
    label = "GST Voucher cash"
    unit = SGD
    definition_period = YEAR
    reference = "https://www.govbenefits.gov.sg/" "about-us/gst-voucher/"

    def formula(person, period, parameters):
        p = parameters(period).gov.mof.gstv.cash
        age = person("age", period)
        citizen = person("is_citizen", period)
        income = person("total_income", period)
        av = person.household("property_annual_value", period)
        n_prop = person("number_of_properties", period)
        eligible = (
            citizen
            & (age >= p.age_minimum)
            & (income <= p.income_ceiling)
            & (av <= p.av_ceiling)
            & (n_prop <= p.max_properties)
        )
        amount = where(
            av <= p.av_lower_threshold,
            p.amount_lower_av,
            p.amount_higher_av,
        )
        return where(eligible, amount, 0)
