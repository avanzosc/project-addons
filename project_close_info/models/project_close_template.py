# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectCloseTemplateLine(models.Model):
    _name = 'project.close.template'
    _description = 'Project Closing Approach Template'

    name = fields.Char(string='Approach', translate=True)
