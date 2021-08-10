# Copyright 2018 Maite Esnal - AvanzOSC
# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError
from odoo.models import expression


class FundingSourceProject(models.Model):
    _name = 'funding.source.project'
    _description = 'Funding Source Project'
    _inherit = ['mail.thread']

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
    yearly_amount = fields.Float(
        string='Yearly Amount', digits=dp.get_precision('Funding'))
    active = fields.Boolean(string='Active', default=True)
    budget_submitted = fields.Float(
        string='Proposed Budget', digits=dp.get_precision('Funding'),
        help='Budget amount proposed', track_visibility='onchange')
    budget_approved = fields.Float(
        string='Approved Budget', digits=dp.get_precision('Funding'),
        help='Budget amount approved', track_visibility='onchange')

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

    @api.multi
    def name_get(self):
        """ name_get() -> [(id, name), ...]

        Returns a textual representation for the records in ``self``.
        By default this is the value of the ``display_name`` field.

        :return: list of pairs ``(id, text_repr)`` for each records
        :rtype: list(tuple)
        """
        results = []
        for record in self:
            super(FundingSourceProject, record).name_get()
            name = '{} - {}'.format(
                record.project_id.name, record.source_id.name)
            if record.year:
                name = '[{}] {}'.format(record.year, name)
            results.append((record.id, name))
        return results

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            domain = []
            sources = self.env['funding.source'].search(
                [('name', operator, name)], limit=limit)
            if sources:
                domain = expression.OR(
                    [[('source_id', 'in', sources.ids)], domain])
            if domain:
                recs = self.search(domain + args, limit=limit)
        return recs.name_get()
