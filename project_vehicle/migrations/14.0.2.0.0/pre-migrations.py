# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if not openupgrade.column_exists(env.cr, "account_analytic_account", "vehicle_id"):
        openupgrade.add_fields(
            env,
            [
                (
                    "vehicle_id",
                    "account.analytic.account",
                    "account_analytic_account",
                    "integer",
                    False,
                    "project_vehicle",
                ),
            ],
        )
    openupgrade.logged_query(
        env.cr,
        """UPDATE account_analytic_account a
            SET vehicle_id = p.vehicle_id
            FROM project_project p
            WHERE a.id = p.analytic_account_id
                AND p.vehicle_id IS NOT NULL
                AND a.vehicle_id IS NULL
                AND a.vehicle_id IS NULL
        """,
    )
