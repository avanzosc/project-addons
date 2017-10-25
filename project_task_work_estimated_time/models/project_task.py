# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    work_ids = fields.One2many(copy=True)

    @api.multi
    def copy(self, default=None):
        return super(ProjectTask,
                     self.with_context(no_analytic_entry=True)).copy(default)


class ProjectTaskWork(models.Model):
    _inherit = 'project.task.work'

    hours = fields.Float(copy=False)
    estimated_time = fields.Float(string='Estimated time', copy=True)
