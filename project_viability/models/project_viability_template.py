# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectViabilityTemplateLine(models.Model):
    _name = 'project.viability.template.line'
    _description = 'Viability Template Line'
    _order = 'categ_id,factor_id'

    templ_id = fields.Many2one(
        comodel_name='project.viability.template', string='Template',
        required=True, ondelete='cascade')
    factor_id = fields.Many2one(
        comodel_name='project.viability.factor', string='Factor',
        required=True)
    categ_id = fields.Many2one(
        comodel_name='project.viability.category', string='Category',
        related='factor_id.categ_id')
    percentage = fields.Float(
        string='Percentage', compute='_compute_percentage')

    _sql_constraints = [
        ('templ_factor_unique', 'unique(templ_id, factor_id)',
         'There should only select the factor once per template.'),
    ]

    @api.depends('templ_id', 'categ_id', 'templ_id.line_ids',
                 'templ_id.line_ids.categ_id')
    def _compute_percentage(self):
        for line in self:
            line.percentage = (
                100 / len(
                    line.mapped('templ_id.line_ids').filtered(
                        lambda l: l.categ_id == line.categ_id)))


class ProjectViabilityTemplateCategoryLine(models.Model):
    _name = 'project.viability.template.category.line'
    _description = 'Viability Template Line'

    templ_id = fields.Many2one(
        comodel_name='project.viability.template', string='Template',
        required=True, ondelete='cascade')
    categ_id = fields.Many2one(
        comodel_name='project.viability.category', string='Category')
    percentage = fields.Float(
        string='Percentage', compute='_compute_percentage')

    @api.depends('templ_id', 'templ_id.categ_line_ids')
    def _compute_percentage(self):
        for line in self:
            line.percentage = (
                100 / len(
                    line.mapped('templ_id.categ_line_ids')))


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
    line_ids = fields.One2many(
        comodel_name='project.viability.template.line',
        inverse_name='templ_id', string='Template Lines')
    categ_line_ids = fields.One2many(
        comodel_name='project.viability.template.category.line',
        inverse_name='templ_id', string='Template Category Lines')

    @api.depends('factor_ids', 'factor_ids.categ_id')
    def _compute_categ_ids(self):
        for templ in self:
            templ.categ_ids = templ.mapped('factor_ids.categ_id')

    @api.model
    def create(self, values):
        res = super(ProjectViabilityTemplate, self).create(values)
        res._reload_categ_line_ids()
        return res

    @api.multi
    def write(self, values):
        res = super(ProjectViabilityTemplate, self).write(values)
        if 'line_ids' in values:
            self._reload_categ_line_ids()
        return res

    @api.multi
    def _reload_categ_line_ids(self):
        for template in self:
            template.categ_line_ids.unlink()
            template.categ_line_ids = [
                (0, 0, {'categ_id': x.id})
                for x in template.mapped('line_ids.categ_id')]
