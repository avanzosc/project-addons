# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


def update_risk_and_oppportunity_active_column(cr):
    cr.execute("""
        UPDATE
          project_risk_table AS risk
        SET
          active = (SELECT active
                    FROM project_project AS project
                    WHERE project.id = risk.project_id);
    """)
    cr.execute("""
        UPDATE
          project_opportunity_table AS opportunity
        SET
          active = (SELECT active
                    FROM project_project AS project
                    WHERE project.id = opportunity.project_id);
    """)


def migrate(cr, version):
    if not version:
        return
    update_risk_and_oppportunity_active_column(cr)
