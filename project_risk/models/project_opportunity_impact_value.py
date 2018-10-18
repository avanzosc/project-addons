# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectOpportunityImpactValue(models.Model):
    _name = 'project.opportunity.impact.value'
    _description = 'Opportunity Impact Values'

    name = fields.Char(string='Name', translate=True, required=True)
    rating = fields.Float(string='Rating')
