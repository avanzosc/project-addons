# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class ProjectIdeaLineViability(models.Model):
    _name = 'project.viability.line'
    _description = 'Viability Line'
    _order = 'project_id, categ_id, factor_id'

    project_id = fields.Many2one(
        string='Project', comodel_name='project.project', required=True)
    factor_id = fields.Many2one(
        comodel_name='project.viability.factor', string='Factor',
        required=True)
    categ_id = fields.Many2one(
        comodel_name='project.viability.category', string='Category',
        related='factor_id.categ_id')
    percentage = fields.Float(
        string='Percentage', compute='_compute_percentage',
        digits=dp.get_precision('Viability Percentage'))
    score = fields.Selection(
        selection=[(0, '0'),
                   (1, '1'),
                   (2, '2'),
                   (3, '3'),
                   (4, '4'),
                   (5, '5')], string='Score', default=0)
    weighted_score = fields.Float(
        string='Weighted Score', compute='_compute_weighted_score',
        digits=dp.get_precision('Viability Score'))

    @api.depends('project_id', 'categ_id', 'project_id.viability_line_ids',
                 'project_id.viability_line_ids.categ_id')
    def _compute_percentage(self):
        for line in self:
            line.percentage = (
                100 / len(
                    line.mapped('project_id.viability_line_ids').filtered(
                        lambda l: l.categ_id == line.categ_id)))

    @api.depends('percentage', 'score')
    def _compute_weighted_score(self):
        for line in self:
            line.weighted_score = (
                line.score * (line.percentage / 100))


class ProjectIdeaCatViability(models.Model):
    _name = 'project.viability.category.line'
    _description = 'Project Viability per Category'
    _order = 'project_id, categ_id'

    project_id = fields.Many2one(
        string='Project', comodel_name='project.project', required=True)
    categ_id = fields.Many2one(
        string='Category', comodel_name='project.viability.category',
        required=True)
    percentage = fields.Float(
        string='Percentage', compute='_compute_percentage',
        digits=dp.get_precision('Viability Percentage'))
    score = fields.Float(
        string='Score', compute='_compute_score',
        digits=dp.get_precision('Viability Score'))
    weighted_score = fields.Float(
        string='Weighted Score', compute='_compute_weighted_score',
        digits=dp.get_precision('Viability Score'))

    @api.depends('project_id', 'project_id.viability_categ_line_ids')
    def _compute_percentage(self):
        for line in self:
            line.percentage = (
                100 / len(
                    line.mapped('project_id.viability_categ_line_ids')))

    @api.depends('project_id', 'categ_id', 'project_id.viability_line_ids')
    def _compute_score(self):
        for line in self:
            line.score = sum(
                line.mapped('project_id.viability_line_ids').filtered(
                    lambda l: l.categ_id == line.categ_id
                ).mapped('weighted_score'))

    @api.depends('percentage', 'score')
    def _compute_weighted_score(self):
        for line in self:
            line.weighted_score = (
                line.score * (line.percentage / 100))
