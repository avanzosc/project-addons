# Copyright 2018 Xanti Pablo - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    funding_ids = fields.One2many(
        comodel_name='funding.source.project', inverse_name='project_id',
        string='Funding Sources')

    @api.onchange('res_area_id')
    def _onchange_area_id(self):
        self.ensure_one()
        self.nonoperative = self.res_area_id.nonoperative

    @api.onchange('res_area_id', 'res_area_type_id')
    def _onchange_area_type(self):
        self.ensure_one()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        manual_code = get_param('project_characterization.manual_code',
                                'False').lower() == 'true'
        if not manual_code:
            if self.res_area_id and self.res_area_type_id:
                try:
                    projects = self.search([
                        ('res_area_id', '=', self.res_area_id.id),
                        ('res_area_type_id', '=', self.res_area_type_id.id)])
                    count = int(sorted(
                        projects.mapped('num_code'), key=int, reverse=True)[0])
                except Exception:
                    count = self.search_count([
                        ('res_area_id', '=', self.res_area_id.id),
                        ('res_area_type_id', '=', self.res_area_type_id.id)])
                self.num_code = count + 1


class ResAreaType(models.Model):
    _inherit = 'res.area.type'

    project_ids = fields.One2many(
        comodel_name='project.project', inverse_name='res_area_type_id',
        string='Projects')


class ResArea(models.Model):
    _inherit = 'res.area'

    nonoperative = fields.Boolean(string='Non Operative')
    related_operative_area_ids = fields.Many2many(
        comodel_name='res.area', relation='rel_nonop2op_area',
        column1='nonop_area_id', column2='op_area_id',
        domain="[('nonoperative', '=', False)]")
