# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr, """
        UPDATE project_task t
        SET active = (
            SELECT p.active
            FROM project_project p
            WHERE p.id = t.project_id)
        WHERE project_id IN (
            SELECT id
            FROM project_project
            WHERE historical_date IS NOT NULL
            OR historical_user_id IS NOT NULL)""")
