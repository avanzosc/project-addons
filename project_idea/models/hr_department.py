# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    randd = fields.Boolean(string='R and D')
