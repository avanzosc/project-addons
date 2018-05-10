# Copyright 2018 Xanti Pablo - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ResAreaType(models.Model):
    _inherit = 'res.area.type'

    project_ids = fields.One2many(
        comodel_name='project.project', inverse_name='res_area_type_id',
        string='Projects')
