# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.addons.account_analytic_billing_plan.tests.\
    test_account_analytic_billing_plan import TestAccountAnalyticBillingPlan


class TestProjectBillingPlan(TestAccountAnalyticBillingPlan):

    @classmethod
    def setUpClass(cls):
        super(TestProjectBillingPlan, cls).setUpClass()
        project_model = cls.env['project.project']
        cls.project = project_model.create({
            'analytic_account_id': cls.analytic.id,
            'name': 'Test Project',
        })

    def test_project_billing_plan_open(self):
        self.assertEqual(self.project.billing_plan_count, 2)
        action_dict = self.project.button_open_billing_plan()
        self.assertEqual(
            action_dict.get('res_model'), 'account.analytic.billing.plan')

    def test_billing_plan(self):
        """Don't repeat this test."""
        pass

    def test_billing_plans(self):
        """Don't repeat this test."""
        pass

    def test_billing_plans_twopartner(self):
        """Don't repeat this test."""
        pass

    def test_billing_plan_onchange_product(self):
        """Don't repeat this test."""
        pass

    def test_billing_plan_onchange_analytic_account(self):
        """Don't repeat this test."""
        pass

    def test_billing_plan_open(self):
        """Don't repeat this test."""
        pass

    def test_billing_plan_invoice_user_error(self):
        """Don't repeat this test."""
        pass

    def test_billing_plan_invoice_line_user_error(self):
        """Don't repeat this test."""
        pass
