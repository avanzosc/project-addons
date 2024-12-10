# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProjectType(models.Model):
    _inherit = "project.type"

    sequence_id = fields.Many2one(string="Sequence", comodel_name="ir.sequence")
