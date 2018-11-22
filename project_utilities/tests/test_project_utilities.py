# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common


class TestProjectUtilities(common.TransactionCase):

    def setUp(self):
        super(TestProjectUtilities, self).setUp()
        project_model = self.env['project.project']
        self.project = project_model.create({
            'name': 'Test Project',
        })

    def test_show_analytic_account(self):
        result = self.project.show_analytic_account_from_project()
        domain = result.get('domain')
        self.assertEquals(domain,
                          [('id', '=', self.project.analytic_account_id.id)])
