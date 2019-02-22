# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.model
    def _get_selection_level(self):
        return self.env['hr.employee.skill'].fields_get(
            allfields=['level'])['level']['selection']

    parent_skill_id = fields.Many2one(
        comodel_name='hr.skill', string='Parent Skill',
        domain="[('child_ids','!=',False)]")
    skill_id = fields.Many2one(
        comodel_name='hr.skill', string='Skill',
        domain="[('parent_id','=',parent_skill_id),('child_ids','=',False)]")
    skill_level = fields.Selection(
        selection='_get_selection_level', string='Skill Level')
    possible_user_ids = fields.Many2many(
        comodel_name='res.users', compute='_compute_possible_user_ids')

    @api.depends('skill_id', 'skill_level')
    def _compute_possible_user_ids(self):
        employee_skill_model = self.env['hr.employee.skill']
        for task in self.filtered(lambda t: t.skill_id):
            employee_by_skill = employee_skill_model.search([
                ('skill_id', '=', task.skill_id.id),
                ('level', '=', task.skill_level),
            ])
            task.possible_user_ids = [
                (6, 0, employee_by_skill.mapped('employee_id.user_id').ids)]

    @api.onchange('parent_skill_id')
    def _onchange_parent_skill_id(self):
        for task in self:
            if task.skill_id.parent_id != task.parent_skill_id:
                task.skill_id = False
                task.skill_level = '0'

    @api.onchange('skill_id', 'skill_level')
    def _onchange_skill_and_level(self):
        for task in self:
            task.user_id = (
                False if task.user_id not in task.possible_user_ids else
                task.user_id)
