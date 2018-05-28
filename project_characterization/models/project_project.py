# Copyright 2018 Xanti Pablo - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tools.safe_eval import safe_eval
from odoo import fields, models
from odoo.osv import expression


class ProjectProject(models.Model):
    _inherit = 'project.project'

    funding_ids = fields.One2many(
        comodel_name='funding.source.project', inverse_name='project_id',
        string='Funding Sources')

    def show_analytic_account_from_project(self):
        action = self.env.ref(
            'analytic.action_account_analytic_account_form')
        action_dict = action.read()[0] if action else {}
        new_domain = [('id', '=', self.analytic_account_id.id)]
        action_dict['domain'] = expression.AND(
            [new_domain, safe_eval(action_dict.get('domain') or '[]')])
        return action_dict


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
