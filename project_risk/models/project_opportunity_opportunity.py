# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectOpportunityOpportunyty(models.Model):
    _name = 'project.opportunity.opportunity'
    _description = 'Opportunity'

    name = fields.Char(string='Name', translate=True)
    description = fields.Text(string='Description', translate=True)
