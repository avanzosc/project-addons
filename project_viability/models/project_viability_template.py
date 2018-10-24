# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectViabilityTemplate(models.Model):
    _name = 'project.viability.template'
    _description = 'Viability Template'

    name = fields.Char(string='Name', required=True, translate=True)
    active = fields.Boolean(string='Active', default=True)
    factor_ids = fields.Many2many(
        comodel_name='project.viability.factor', string='Factors',
        relation='viability_templ_factor_rel', column1='templ_id',
        column2='factor_id')
    categ_ids = fields.Many2many(
        comodel_name='project.viability.category', string='Categories',
        compute='_compute_categ_ids')

    @api.depends('factor_ids', 'factor_ids.categ_id')
    def _compute_categ_ids(self):
        for templ in self:
            templ.categ_ids = templ.mapped('factor_ids.categ_id')
