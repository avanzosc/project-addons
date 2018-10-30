# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    historical_date = fields.Date(string='Historical Date', readonly=True)
    version = fields.Integer(string='Version', copy=False, default=1)
    parent_id = fields.Many2one(
        comodel_name='project.project', string='Parent Project', copy=False)
    old_version_ids = fields.Many2many(
        comodel_name='project.project', string='Old Versions',
        compute='_compute_old_versions')

    @api.multi
    def _compute_old_versions(self):
        for project in self:
            parent = project.parent_id
            old_version = self.env['project.project']
            while parent:
                old_version += parent
                parent = parent.parent_id
            project.old_version_ids = old_version

    @api.multi
    def button_new_version(self):
        self.ensure_one()
        new_project = self._copy_project()
        self.button_historical()
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form, tree',
            'view_mode': 'form',
            'res_model': 'project.project',
            'res_id': new_project.id,
            'target': 'current',
        }

    def _copy_project(self):
        # active_draft = self.env['mrp.config.settings']._get_parameter(
        #     'active.draft')
        new_project = self.copy({
            'name': self.name,
            'version': self.version + 1,
            # 'active': active_draft and active_draft.value or False,
            'parent_id': self.id,
        })
        return new_project

    @api.multi
    def button_historical(self):
        self.write({
            # 'active': False,
            # 'state': 'historical',
            'historical_date': fields.Date.today()
        })
