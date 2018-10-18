# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectOpportunityAction(models.Model):
    _name = 'project.opportunity.action'
    _description = 'Opportunity Action'

    name = fields.Char(string='Name', translate=True, required=True)
    description = fields.Char(string='Description', translate=True)
