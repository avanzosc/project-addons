# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tools.safe_eval import safe_eval
from odoo import api, fields, models
from odoo.osv import expression

from dateutil.relativedelta import relativedelta

str2datetime = fields.Datetime.from_string


class ProjectProject(models.Model):
    _inherit = 'project.project'

    def show_analytic_account_from_project(self):
        action = self.env.ref(
            'analytic.action_account_analytic_account_form')
        action_dict = action.read()[0] if action else {}
        new_domain = [('id', '=', self.analytic_account_id.id)]
        action_dict['domain'] = expression.AND(
            [new_domain, safe_eval(action_dict.get('domain') or '[]')])
        return action_dict


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.multi
    def _change_project_task_date(self, new_days):
        if not new_days:
            return
        for task in self:
            vals = {}
            deltadays = relativedelta(days=new_days)
            if task.date_start:
                vals['date_start'] = str2datetime(task.date_start) + deltadays
            if task.date_end:
                vals['date_end'] = str2datetime(task.date_end) + deltadays
            if vals:
                task.write(vals)
