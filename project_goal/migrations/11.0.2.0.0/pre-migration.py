# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


def update_goal_active_column(cr):
    cr.execute("""
        UPDATE
          project_goal AS goal
        SET
          active = (SELECT active
                    FROM project_project AS project
                    WHERE project.id = goal.project_id);
    """)


def migrate(cr, version):
    if not version:
        return
    update_goal_active_column(cr)
