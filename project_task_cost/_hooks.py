# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import SUPERUSER_ID
from odoo.api import Environment


def post_init_hook(cr, pool):
    env = Environment(cr, SUPERUSER_ID, {})
    for task in env['project.task'].search([]):
        task._onchange_user()
    env['account.analytic.line'].search([
        ('employee_id', '!=', False)]).create_calendar()
