# Copyright 2018 Maite Esnal - AvanzOSC
# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError


class FundingSource(models.Model):
    _name = 'funding.source'
    _description = 'Funding Source'

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    grant = fields.Char(string='Grant')  # SUBVENCION
    soft_credit = fields.Char(string='Soft Credit')  # credito blando
    mixed_credit = fields.Char(string='Mixed Credit')  # credito mixto
    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Partner')
    funding_account_id = fields.Many2one(
        comodel_name='account.account', string='Funding Source Account')
    type_id = fields.Many2one(
        comodel_name='funding.source.type', string='Funding Type')


class FundingSourceType(models.Model):
    _name = 'funding.source.type'
    _description = 'Funding Source Type'

    name = fields.Char(string='Name')


class FundingSourceProject(models.Model):
    _name = 'funding.source.project'
    _description = 'Funding Source Project'

    project_id = fields.Many2one(
        comodel_name='project.project', string='Project', required=True)
    source_id = fields.Many2one(
        comodel_name='funding.source', string='Funding Source', required=True)
    account_id = fields.Many2one(
        comodel_name='account.account', string='Funding Source Account')
    percentage = fields.Float(
        string='Percentage (%)', digits=dp.get_precision('Discount'),
        group_operator='sum')
    funding_date = fields.Date(string='Funding Date')
    year = fields.Integer(string='Year')
    yearly_amount = fields.Float(string='Yearly Amount', digits=0)

    @api.multi
    @api.constrains('percentage')
    def _check_discount(self):
        for line in self:
            if line.percentage < 0:
                raise ValidationError(
                    _("Percentage must be bigger than 0"))
            elif line.percentage > 100:
                raise ValidationError(
                    _("Percentage should be less or equal to 100"))
