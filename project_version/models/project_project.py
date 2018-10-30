# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    historical_date = fields.Date(string='Historical Date', readonly=True)
    historical_user_id = fields.Many2one(
        comodel_name='res.users', string='Historifying User', readonly=True)
    version_date = fields.Date(string='Version Date', readonly=True)
    version_user_id = fields.Many2one(
        comodel_name='res.users', string='Versioning User', readonly=True)
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
        self._copy_project()
        revno = self.version
        self.write({
            'version': revno + 1,
            'version_date': fields.Date.today(),
            'version_user_id': self.env.user.id,
        })

    def _copy_project(self):
        new_test = self.copy({
            'version': self.version,
            'name': self.name,
            'parent_id': self.id,
        })
        new_test.button_historical()
        return new_test

    @api.multi
    def button_historical(self):
        self.write({
            'active': False,
            'historical_date': fields.Date.today(),
            'historical_user_id': self.env.user.id,
        })
