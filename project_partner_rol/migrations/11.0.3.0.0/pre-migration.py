# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


def update_participant_active_column(cr):
    cr.execute("""
        UPDATE
          project_participant AS participant
        SET
          active = (SELECT active
                    FROM project_project AS project
                    WHERE project.id = participant.project_id);
    """)


def migrate(cr, version):
    if not version:
        return
    update_participant_active_column(cr)
