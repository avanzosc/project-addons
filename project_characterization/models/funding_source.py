# Copyright 2018 Maite Esnal - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


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


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.depends
    def _funding_source_count(self):
        for partner in self:
            partner.funding_source_count = len(partner.funding_source_ids)

    funding_source_ids = fields.One2many(comodel_name='funding.source',
                                         string='Funding Sources',
                                         inverse_name='partner_id')
    funding_source_count = fields.Integer(string='Funding Sources',
                                          compute=_funding_source_count)
    areas = fields.Many2many(
        string="Areas", comodel_name="project.area",
        relation="partner_area_relation", columm1="partner_idproject_area_id",
        columm2='project_area_id', copy=False)


