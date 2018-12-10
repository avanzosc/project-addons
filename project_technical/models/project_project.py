# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    customer_goal = fields.Char(string="Customer's Goal")
    internal_goal = fields.Char(string='Internal Goal')
    work_scope = fields.Text(string='Scope of Work')
    definition = fields.Text(string='Technical Definition')
    task_description = fields.Html(string='Description of Tasks')
