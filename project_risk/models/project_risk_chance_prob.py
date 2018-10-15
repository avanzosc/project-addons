# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectRiskChanceProb(models.Model):
    _name = 'project.risk.chance.prob'

    name = fields.Char(string='Name', translate=True)
    qualification = fields.Float(string='Qualification')
