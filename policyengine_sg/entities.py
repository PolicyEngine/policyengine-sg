"""
Entity definitions for the Singapore tax and benefit system.

References:
- Inland Revenue Authority of Singapore: https://www.iras.gov.sg/
- Central Provident Fund Board: https://www.cpf.gov.sg/
- Ministry of Social and Family Development: https://www.msf.gov.sg/
- Ministry of Manpower: https://www.mom.gov.sg/
"""

from policyengine_core.entities import build_entity


Person = build_entity(
    key="person",
    plural="people",
    label="Person",
    doc="""
    An individual person in Singapore.
    
    This is the base entity for all individual-level calculations including
    income tax, CPF contributions, and individual social assistance payments.
    """,
    is_person=True,
)


TaxUnit = build_entity(
    key="tax_unit",
    plural="tax_units",
    label="Tax unit",
    doc="""
    A Singapore tax filing unit.
    
    In Singapore, individuals generally file taxes separately, but there are
    some provisions for married couples (e.g., wife relief, child relief).
    This entity represents a tax assessment unit.
    
    Reference: https://www.iras.gov.sg/taxes/individual-income-tax
    """,
    containing_entities=["household"],
    roles=[
        {
            "key": "primary",
            "plural": "primaries",
            "label": "Primary taxpayer",
            "doc": "The primary person filing the tax return",
        },
        {
            "key": "spouse",
            "plural": "spouses",
            "label": "Spouse",
            "doc": "The spouse of the primary taxpayer (if applicable)",
            "max": 1,
        },
        {
            "key": "dependent",
            "plural": "dependents",
            "label": "Dependent",
            "doc": "Dependent children or other dependents",
        },
    ],
)


CPFUnit = build_entity(
    key="cpf_unit",
    plural="cpf_units",
    label="CPF unit",
    doc="""
    A Central Provident Fund assessment unit.
    
    This represents the unit used for CPF contributions and withdrawals.
    CPF accounts are individual-based but family relationships affect
    certain schemes (e.g., CPF Housing Scheme, Medisave).
    
    Reference: https://www.cpf.gov.sg/member/account-services
    """,
    containing_entities=["household"],
    roles=[
        {
            "key": "member",
            "plural": "members",
            "label": "CPF member",
            "doc": "Individual CPF account holder",
        },
        {
            "key": "nominee",
            "plural": "nominees",
            "label": "Nominee",
            "doc": "Person nominated to receive CPF benefits",
        },
    ],
)


BenefitUnit = build_entity(
    key="benefit_unit",
    plural="benefit_units",
    label="Benefit unit",
    doc="""
    A social assistance assessment unit for ComCare and other programs.
    
    This represents the unit used to assess eligibility and calculate benefits
    for Singapore's social assistance programs. It typically includes a person,
    their spouse (if applicable), and dependent children.
    
    Reference: https://www.msf.gov.sg/assistance/comcare
    """,
    containing_entities=["household"],
    roles=[
        {
            "key": "adult",
            "plural": "adults",
            "label": "Adult",
            "doc": "Adult member of the benefit unit",
            "max": 2,
        },
        {
            "key": "child",
            "plural": "children",
            "label": "Child",
            "doc": "Dependent child in the benefit unit",
        },
    ],
)


Household = build_entity(
    key="household",
    plural="households",
    label="Household",
    doc="""
    A physical household in Singapore.
    
    This represents all people living at the same address, used for
    household-level calculations such as utilities subsidies and some
    means testing provisions for social programs.
    
    Reference: https://www.singstat.gov.sg/find-data/search-by-theme/households
    """,
    roles=[
        {
            "key": "member",
            "plural": "members",
            "label": "Member",
            "doc": "A person living in the household",
        },
    ],
)


entities = [Person, TaxUnit, CPFUnit, BenefitUnit, Household]