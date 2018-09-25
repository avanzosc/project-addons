# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models, api


class MaterialResources(models.Model):
    _name = 'project.idea.resource.material'

    project_id = fields.Many2one(
        string='Project', comodel_name='project.project', required=True)
    product_id = fields.Many2one(
        string='Product', comodel_name='product.product')
    product_name = fields.Char(string='Product Name')
    product_intensity = fields.Selection(
        selection=[('high', 'High'),
                   ('medium', 'Medium'),
                   ('low', 'Low')], string='Intensity')

    @api.onchange('product_id')
    def onchange_product_id(self):
        self.product_name = self.product_id.name
