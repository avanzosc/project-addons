# Copyright (c) 2022 Alfredo de la Fuente - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    sale_type_id = fields.Many2one(
        string="Sale type",
        comodel_name="sale.order.type",
        related="sale_order_id.type_id",
        store=True,
        copy=False,
    )
