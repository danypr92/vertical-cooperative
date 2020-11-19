# Copyright 2020 - ongoing Coop IT Easy SCRLfs (<http://www.coopiteasy.be>)
# - Houssine BAKKALI - <houssine@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Easy My Coop Loan Account",
    "version": "12.0.1.0.0",
    "depends": [
        "account",
        "easy_my_coop_loan",
        ],
    "author": "Coop IT Easy SCRLfs",
    "category": "Cooperative management",
    "website": "https://www.coopiteasy.be",
    "license": "AGPL-3",
    "summary": """
    This module brings the accounting part of the loan issue.
    It has for purpose to generate all the  accounting entries to the covered
    use cases.
    """,
    "data": [
        "data/emc_loan_account_data.xml",
        "views/res_company_view.xml",
        "views/loan_issue_line_view.xml",
    ],
    "installable": True,
}