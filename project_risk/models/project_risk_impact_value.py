# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectRiskImpactValue(models.Model):
    _name = 'project.risk.impact.value'

    name = fields.Char(string='Impact')
    rating = fields.Float(string='Rating')
