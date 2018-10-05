# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


def update_budget_date(cr):
    cr.execute("""
        ALTER TABLE
          crossovered_budget
        ADD COLUMN
          budget_date date;
    """)
    cr.execute("""
        UPDATE
          crossovered_budget
        SET
          budget_date = create_date;
    """)


def migrate(cr, version):
    if not version:
        return
    update_budget_date(cr)
