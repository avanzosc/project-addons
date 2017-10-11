# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class WizProjectTaskMerge(models.TransientModel):

    _name = 'wiz.project.task.merge'
    _description = "Wizard for task merge"

    name = fields.Char(string='Description')

    @api.multi
    def merge_tasks(self):
        task_obj = self.env['project.task']
        tasks = task_obj.browse(self.env.context.get('active_ids'))
        tasks._merge_tasks_from_wizard()
