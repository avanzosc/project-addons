# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr, """
        UPDATE account_analytic_account acc
        SET active = (
        SELECT active FROM project_project WHERE analytic_account_id = acc.id)
        WHERE id IN (SELECT analytic_account_id FROM project_project)"""
    )
