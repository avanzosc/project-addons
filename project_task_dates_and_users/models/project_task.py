# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    date_done = fields.Date(string="Date done")
    revised_date = fields.Date(string="Revised date")
    user_date_done_id = fields.Many2one(
        string="User date done",
        compute="_compute_user_date_done_id",
        comodel_name="res.partner",
        store=True,
    )
    user_revised_date_id = fields.Many2one(
        string="User revised date",
        compute="_compute_user_revised_date_id",
        comodel_name="res.partner",
        store=True,
    )

    @api.depends("date_done")
    def _compute_user_date_done_id(self):
        for task in self.filtered(lambda x: x.date_done):
            task.user_date_done_id = self.env.user.partner_id.id

    @api.depends("revised_date")
    def _compute_user_revised_date_id(self):
        for task in self.filtered(lambda x: x.revised_date):
            task.user_revised_date_id = self.env.user.partner_id.id
