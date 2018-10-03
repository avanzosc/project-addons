# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectIdeaViabilityCategory(models.Model):
    _name = 'project.idea.viability.category'
    _description = 'Viability Category'

    name = fields.Char(string='Name')
