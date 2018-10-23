# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectIdeaCatViability(models.Model):
    _name = 'project.idea.cat.viability'
    _description = 'Project Viability per Category'

    project_id = fields.Many2one(
        string='Project', comodel_name='project.project', required=True)
    category_id = fields.Many2one(
        string='Category', comodel_name='project.idea.viability.category')
    cat_percentage = fields.Float(string='Percentage')
    cat_punctuation = fields.Float(string='Punctuation')
    cat_pondered = fields.Char(string='Weighted Score')

    @api.depends('cat_percentage', 'cat_punctuation')
    def _compute_cat_pondered(self):
        for line in self:
            line.cat_pondered = (
                (line.cat_percentage / 100) * line.cat_punctuation)
