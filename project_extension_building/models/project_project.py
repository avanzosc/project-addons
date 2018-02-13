# Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'
    # _rec_name = 'project_id'
    #
    # project_id = fields.Many2one(
    #     comodel_name='project.project', string='Project')
    management_type = fields.Selection(
        selection=[
            ('assessment', 'Risk assessment'),
            ('plan', 'Security plan'),
        ], string='Management Type')
    workers_qty = fields.Integer(string='Nº of workers')
    max_male_workers_qty = fields.Integer(string='Max. Male Workers Qty')
    max_female_workers_qty = fields.Integer(string='Max. Female Workers Qty')
    builded_surface = fields.Float(string='Builded surface')
    building_height = fields.Float(string='Building height')
    budget_material = fields.Float(string='Budget execution material')
    init_date = fields.Datetime(string='Initial date of work')
    init_date_unit_id = fields.Many2one(
        comodel_name='product.uom', string='Initial date unit')
    duration_time = fields.Integer(string='Duration time')
    duration_time_unit_id = fields.Many2one(
        comodel_name='product.uom', string='Duration time unit')
    contract_time = fields.Integer(string='Contract time')
    work_workers = fields.Integer(string='Work workers')
    work_workers_unit_id = fields.Many2one(
        comodel_name='product.uom', string='Work workers unit')
    freelance_qty = fields.Integer(string='Nº freelance')
    center_open_date = fields.Datetime(string='Open date')
    waste_estimation = fields.Integer(string='Waste estimation')
    waste_estimation_unit_id = fields.Many2one(
        comodel_name='product.uom', string='Waste estimation unit')
    freelance_tax = fields.Selection(
        selection=[
            ('passive', 'passive subject'),
            ('normal', 'normal_subject')
        ]
    )
    work_type_id = fields.Many2one(
        comodel_name='work.type', string='Work Type')
    license_number = fields.Char(string='Nº of License')


class WorkType(models.Model):
    _name = 'work.type'

    name = fields.Char(string='Name')
