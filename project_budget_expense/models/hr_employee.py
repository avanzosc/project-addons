# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    property_account_payable_id = fields.Many2one(
        comodel_name='account.account', company_dependent=True,
        string="Account Payable",
        domain="[('internal_type', '=', 'payable'),"
               " ('deprecated', '=', False)]",
        related='address_home_id.property_account_payable_id')
    property_account_receivable_id = fields.Many2one(
        comodel_name='account.account', company_dependent=True,
        string="Account Receivable",
        domain="[('internal_type', '=', 'receivable'),"
               " ('deprecated', '=', False)]",
        related='address_home_id.property_account_receivable_id')
