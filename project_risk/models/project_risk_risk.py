# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectRiskRisk(models.Model):
    _name = 'project.risk.risk'

    name = fields.Char(string='Name')
    description = fields.Char(string='Description')
