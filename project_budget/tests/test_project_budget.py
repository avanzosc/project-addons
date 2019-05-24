# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common
from odoo import exceptions, fields

from_string = fields.Date.from_string
to_string = fields.Date.to_string


class TestProjectBudget(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProjectBudget, cls).setUpClass()
        cls.project_model = cls.env['project.project']
        cls.wizard = cls.env['project.initial.budget']
        cls.search_model = cls.env['project.budget.search']
        set_param = cls.env['ir.config_parameter'].sudo().set_param
        set_param(
            'account_budget_template.budget_template_id',
            cls.env.ref('project_budget.project_budget_template').id)
        set_param('project_budget.summary_line', True)
        cls.project = cls.project_model.create({
            'name': 'New Project',
        })

    def test_project_creation(self):
        self.assertTrue(self.project.budget_ids)
        self.assertTrue(self.project.budget_ids[:1].initial)
        self.assertEquals(
            len(self.project.budget_ids), self.project.budget_count)
        self.assertTrue(self.project.has_current_budget)
        self.assertIn(
            self.project,
            self.project.search([('has_current_budget', '=', True)]))
        self.assertEquals(len(
            self.project.mapped('budget_ids.crossovered_budget_line')), 26)
        self.project.create_initial_project_budget()
        self.assertEquals(len(self.project.budget_ids), 1)
        action_dict = self.project.budget_ids[:1].open_pivot_view()
        self.assertEquals(action_dict.get('view_mode'), 'pivot')

    def test_initial_budget_per_project_year(self):
        new_budget = self.project.budget_ids.copy()
        with self.assertRaises(exceptions.ValidationError):
            new_budget.initial = True

    def test_budget_line_creation(self):
        self.assertEqual(
            self.project.analytic_account_id.crossovered_budget_line,
            self.project.budget_ids.crossovered_budget_line)
        new_budget = self.project.budget_ids.copy(default={
            'crossovered_budget_line': [],
        })
        new_budget.date_to = from_string(fields.Date.today()).replace(
            month=12, day=29)
        new_budget.button_compute_lines()
        self.assertEquals(len(
            new_budget.crossovered_budget_line), 24)
        self.assertEqual(
            self.project.analytic_account_id.crossovered_budget_line,
            new_budget.crossovered_budget_line)

    def test_initial_budget_duplication(self):
        old_budget = self.project.budget_ids[:1]
        self.assertFalse(
            old_budget.crossovered_budget_line[:1].initial_budget_line_id)
        old_budget.crossovered_budget_line[:1].write({
            'planned_amount': 50.0,
        })
        self.assertEquals(
            old_budget.crossovered_budget_line[:1].sum_amount,
            old_budget.crossovered_budget_line[:1].planned_amount +
            old_budget.crossovered_budget_line[:1].practical_amount)
        new_budget = old_budget.copy()
        self.assertEquals(
            len(old_budget.crossovered_budget_line),
            len(new_budget.crossovered_budget_line))
        new_budget.crossovered_budget_line[:1].write({
            'planned_amount': 150.0,
        })
        self.assertNotEquals(
            new_budget.crossovered_budget_line[:1],
            new_budget.crossovered_budget_line[:1].initial_budget_line_id)
        self.assertEquals(
            old_budget.crossovered_budget_line[:1],
            new_budget.crossovered_budget_line[:1].initial_budget_line_id)
        self.assertEquals(
            old_budget.crossovered_budget_line[:1].planned_amount,
            new_budget.crossovered_budget_line[:1].initial_planned_amount)
        self.assertNotEquals(
            new_budget.crossovered_budget_line[:1].planned_amount,
            new_budget.crossovered_budget_line[:1].initial_planned_amount)
        self.assertEquals(
            new_budget.crossovered_budget_line[:1].sum_amount,
            new_budget.crossovered_budget_line[:1].planned_amount +
            new_budget.crossovered_budget_line[:1].practical_amount)
        self.assertNotEquals(
            old_budget.crossovered_budget_line[:1].sum_amount,
            new_budget.crossovered_budget_line[:1].sum_amount)

    def test_initial_budget_wizard(self):
        today = from_string(fields.Date.today())
        self.assertEquals(len(self.project.budget_ids), 1)
        wizard = self.wizard.with_context(
            active_ids=[self.project.id]).create({
                'date': today.replace(year=today.year + 1),
            })
        self.assertIn(self.project, wizard.project_ids)
        wizard.create_initial_project_budget()
        self.assertEquals(len(self.project.budget_ids), 2)

    def test_search_project_budget(self):
        wizard = self.search_model.create({
            'min_date': fields.Date.today(),
            'max_date': fields.Date.today(),
            'initial_budget': True,
        })
        action_dict = wizard.search_project_not_in_budget()
        self.assertIn(
            ('id', 'not in', self.project.ids), action_dict.get('domain'))
        action_dict = wizard.search_project_in_budget()
        self.assertIn(
            ('id', 'in', self.project.ids), action_dict.get('domain'))
