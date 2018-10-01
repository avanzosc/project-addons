# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectIdeaLineViability(models.Model):
    _name = 'project.idea.line.viability'

    project_id = fields.Many2one(
        string='Project', comodel_name='project.project')
    feasibility_id = fields.Many2one(
        string='Feasibility Category',
        comodel_name='project.idea.viability.category')
    name = fields.Text(string='Name')
    percentage = fields.Float(string='Percentage')
    line_punctuation = fields.Selection(
        selection=[('1', '1'),
                   ('2', '2'),
                   ('3', '3'),
                   ('4', '4'),
                   ('5', '5')], string='Punctuation')
    weighted_score = fields.Char(string='Weighted Score')
    formula_punctuation = fields.Char(string='Formulated Score')
