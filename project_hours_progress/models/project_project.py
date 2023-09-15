# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    all_task_ids = fields.One2many(
        string="All task", comodel_name="project.task", copy=False,
        inverse_name="project_id")
    tasks_planned_hours = fields.Float(
        string="Initially Tasks Planned Hours", tracking=True, store=True,
        copy=False, compute="_compute_tasks_hours_info")
    tasks_real_hours = fields.Float(
        string="Tasks Real Hours", tracking=True, store=True,
        copy=False, compute="_compute_tasks_hours_info")
    tasks_progress = fields.Float(
        string="Tasks Progress", compute="_compute_tasks_hours_info",
        store=True, copy=False, group_operator="avg")
    milestones_percentages = fields.Float(
        string="Total milestones percentages", tracking=True, store=True,
        copy=False, compute="_compute_milestones_percentages")
    milestones_percentages_solved = fields.Float(
        string="Total milestones percentages solved", tracking=True, store=True,
        copy=False, compute="_compute_milestones_percentages")
    milestones_progress = fields.Float(
        string="Milestones Progress", compute="_compute_milestones_percentages",
        store=True, copy=False, group_operator="avg")

    @api.depends("all_task_ids", "all_task_ids.planned_hours",
                 "all_task_ids.timesheet_ids",
                 "all_task_ids.timesheet_ids.unit_amount")
    def _compute_tasks_hours_info(self):
        for project in self:
            tasks_planned_hours = 0
            tasks_real_hours = 0
            tasks_progress = 0
            if project.all_task_ids:
                tasks_planned_hours = sum(
                    project.all_task_ids.mapped("planned_hours"))
                for task in project.all_task_ids:
                    if task.timesheet_ids:
                        tasks_real_hours += sum(
                            task.timesheet_ids.mapped("unit_amount"))
            if tasks_planned_hours > 0:
                if tasks_real_hours > tasks_planned_hours:
                    tasks_progress = 100
                else:
                    tasks_progress = round(
                        100.0 * tasks_real_hours / tasks_planned_hours, 2)
            project.tasks_planned_hours = tasks_planned_hours
            project.tasks_real_hours = tasks_real_hours
            project.tasks_progress = tasks_progress

    @api.depends("milestone_ids", "milestone_ids.quantity_percentage",
                 "milestone_ids.is_reached")
    def _compute_milestones_percentages(self):
        for project in self:
            milestones_percentages = 0
            milestones_percentages_solved = 0
            milestones_progress = 0
            if project.milestone_ids:
                milestones_percentages = sum(
                    project.milestone_ids.mapped("quantity_percentage"))
                milestones_percentages = milestones_percentages * 100
                milestones_reached = project.milestone_ids.filtered(
                    lambda x: x.is_reached)
                if milestones_reached:
                    milestones_percentages_solved = sum(
                        milestones_reached.mapped("quantity_percentage"))
                    milestones_percentages_solved = (
                        milestones_percentages_solved * 100)
            if milestones_percentages > 0:
                if milestones_percentages_solved > milestones_percentages:
                    milestones_progress = 100
                else:
                    milestones_progress = round(
                        100.0 * milestones_percentages_solved /
                        milestones_percentages, 2)
            project.milestones_percentages = milestones_percentages
            project.milestones_percentages_solved = (
                milestones_percentages_solved)
            project.milestones_progress = milestones_progress
