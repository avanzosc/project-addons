# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    historical_date = fields.Date(string='Historified on', readonly=True)
    historical_user_id = fields.Many2one(
        comodel_name='res.users', string='Historified by', readonly=True)
    version_date = fields.Date(
        string='Versioned on', readonly=True, copy=False,
        default=fields.Date.context_today)
    version_user_id = fields.Many2one(
        comodel_name='res.users', string='Versioned by', readonly=True,
        copy=False, default=lambda self: self.env.user)
    version = fields.Integer(
        string='Version', readonly=True, copy=False, default=1)
    parent_id = fields.Many2one(
        comodel_name='project.project', string='Parent Project', copy=False)

    def name_get(self):
        res = []
        for project in self:
            if project.historical_date or project.historical_user_id:
                name = _('{}-Historical').format(project.name)
            else:
                name = project.name
            res.append((project.id, name))
        return res

    @api.multi
    def write(self, values):
        res = super(ProjectProject, self).write(values)
        return res

    @api.multi
    def button_new_version(self):
        self.ensure_one()
        if self.historical_date or self.historical_user_id or not self.active:
            return False
        self._copy_project()
        revno = self.version
        self.write({
            'version': revno + 1,
            'version_date': fields.Date.today(),
            'version_user_id': self.env.user.id,
        })

    def _get_copy_data(self):
        return {
            'version': self.version,
            'version_date': self.version_date,
            'version_user_id': self.version_user_id.id,
            'name': self.name,
            'parent_id': self.id,
            'active': False,
        }

    def _copy_project(self):
        vals = self._get_copy_data()
        new_test = self.copy(default=vals)
        return new_test

    @api.multi
    def button_historical(self):
        self.ensure_one()
        if self.historical_date or self.historical_user_id or not self.active:
            return False
        copy = self._copy_project()
        copy.write({
            'historical_date': fields.Date.today(),
            'historical_user_id': self.env.user.id,
        })
