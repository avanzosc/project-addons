# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    confirmed_delivery_date = fields.Date(copy=False)
    real_delivery_date = fields.Date(copy=False)
    validation_date = fields.Date(copy=False)
