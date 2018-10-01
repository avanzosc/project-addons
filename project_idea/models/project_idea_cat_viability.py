# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectIdeaCatViability(models.Model):
    _name = 'project.idea.cat.viability'

    project_id = fields.Many2one(
        string='Project', comodel_name='project.project')
    category_id = fields.Many2one(
        string='Category', comodel_name='project.idea.viability.category')
    cat_percentage = fields.Char(string='Percentage')
    cat_punctuation = fields.Selection(
        selection=[('1', '1'),
                   ('2', '2'),
                   ('3', '3'),
                   ('4', '4'),
                   ('5', '5')], string='Punctuation')
    cat_pondered = fields.Char(string='Weighted Score')
