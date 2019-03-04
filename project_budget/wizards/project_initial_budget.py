# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProjectInitialBudget(models.TransientModel):
    _name = 'project.initial.budget'
    _description = 'Wizard to create initial budget'

    project_ids = fields.Many2many(
        comodel_name='project.project', string='Project')
    date = fields.Date(
        string='Budget Date', default=lambda s: fields.Date.context_today(s))

    @api.model
    def default_get(self, fields):
        rec = super(ProjectInitialBudget, self).default_get(fields)
        rec.update({
            'project_ids': [(6, 0, self.env.context.get('active_ids'))],
        })
        return rec

    @api.multi
    def create_initial_project_budget(self):
        self.ensure_one()
        self.project_ids.create_initial_project_budget(date=self.date)
