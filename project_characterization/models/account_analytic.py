# Copyright 2018 Maite Esnal - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    res_area_id = fields.Many2one(
        comodel_name='res.area', string='Area')
    op_space_id = fields.Many2one(
        comodel_name='res.opportunity.space', string='Opportunity Space')
    res_character_id = fields.Many2one(
        comodel_name='res.character', string='Character')
    justification_deadline = fields.Date(string='Justification Deadline')
    res_area_type_id = fields.Many2one(
        comodel_name='res.area.type', string='Area type',
        domain="[('area_ids', 'in', res_area_id)]")
    res_team_id = fields.Many2one(
        comodel_name='res.team', string='Team')
    res_target_id = fields.Many2one(
        comodel_name='res.target', string='Target')
    nonoperative = fields.Boolean(
        string='Non Operative', related='res_area_id.nonoperative', store=True)
    num_code = fields.Char(string='Number', copy=False)

    @api.onchange('res_area_id', 'res_area_type_id')
    def _onchange_area_type(self):
        self.ensure_one()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        manual_code = get_param('project_characterization.manual_code',
                                'False').lower() == 'true'
        if not manual_code:
            if self.res_area_id and self.res_area_type_id:
                try:
                    count = self.search([
                        ('res_area_id', '=', self.res_area_id.id),
                        ('res_area_type_id', '=', self.res_area_type_id.id)],
                        limit=1, order='num_code DESC')
                    count = int(count.num_code)
                except Exception:
                    count = self.search_count([
                        ('res_area_id', '=', self.res_area_id.id),
                        ('res_area_type_id', '=', self.res_area_type_id.id)])
                self.num_code = count + 1

    @api.model
    def create(self, values):
        if not values.get('code'):
            area_id = values.get('res_area_id')
            type_id = values.get('res_area_type_id')
            num_code = values.get('num_code')
            if area_id and type_id:
                values.update({
                    'code': '{}.{}.{}'.format(
                        self.env['res.area'].browse(area_id).code or '',
                        self.env['res.area.type'].browse(type_id).code or '',
                        num_code or '')
                })
        return super(AccountAnalyticAccount, self).create(values)


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    nonoperative = fields.Boolean(
        string='Non Operative', related='account_id.nonoperative', store=True,
        compute_sudo=True)
