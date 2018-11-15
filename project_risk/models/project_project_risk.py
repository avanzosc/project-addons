# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectProjectRisk(models.Model):
    _inherit = 'project.project'

    risk_table_ids = fields.One2many(
        comodel_name='project.risk.table', inverse_name='project_id',
        copy=True)
    risk_chance_table_ids = fields.One2many(
        comodel_name='project.opportunity.table', inverse_name='project_id')

    @api.multi
    def write(self, vals):
        res = super(ProjectProjectRisk, self).write(vals) if vals else True
        if 'active' in vals:
            # archiving/unarchiving a project does it on its goals, too
            self.with_context(active_test=False).mapped(
                'risk_table_ids').write(
                {'active': vals['active']})
            self.with_context(active_test=False).mapped(
                'risk_chance_table_ids').write(
                {'active': vals['active']})
        return res
