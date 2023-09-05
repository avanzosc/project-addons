from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _name = "project.task.timesheet.report"
    _description = "Task Timesheet Statistics"
    _auto = False
    # _rec_name = 'invoice_date'
    # _order = 'invoice_date desc'

    task_id = fields.Many2one(comodel_name="project.task", readonly=True)
    project_id = fields.Many2one(comodel_name="project.project", readonly=True)
    employee_id = fields.Many2one(comodel_name="hr.employee", readonly=True)
    unit_amount = fields.Float(string="Quantity", readonly=True)

    _depends = {
        "account.analytic.line": [
            "project_id",
            "task_id",
            "employee_id",
            "unit_amount",
        ],
    }

    @property
    def _table_query(self):
        return "%s %s %s %s" % (
            self._select(),
            self._from(),
            self._where(),
            self._group_by(),
        )

    def _select(self):
        return """
            SELECT
              row_number() OVER () AS id,
              line.project_id,
              line.task_id,
              line.employee_id,
              SUM(line.unit_amount) as unit_amount
        """

    def _from(self):
        return """
            FROM account_analytic_line line
        """

    def _where(self):
        return """
            WHERE line.project_id IS NOT NULL
        """

    def _group_by(self):
        group_by_str = """
            GROUP BY
                line.project_id,
                line.task_id,
                line.employee_id
        """
        return group_by_str
