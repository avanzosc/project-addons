# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectRiskProbabilityValue(models.Model):
    _name = 'project.risk.probability.value'

    name = fields.Char(string='Probability')
    rating = fields.Float(string='Rating')
