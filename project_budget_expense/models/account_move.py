# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.multi
    def unlink(self):
        """ unlink()

        Deletes the records of the current set

        :raise AccessError:
            * if user has no unlink rights on the requested object
            * if user tries to bypass access rules for unlink on the requested
              object
        :raise UserError: if the record is default property for other records

        """
        analytic_lines = self.env['account.analytic.line'].search([
            ('move_id', 'in', self.ids), ('employee_id', '=', False)])
        analytic_lines.unlink()
        return super(AccountMove, self).unlink()


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.multi
    def create_analytic_lines(self):
        """ Create analytic items upon validation of an account.move.line
            having an analytic account. This method first remove any existing
            analytic item related to the line before creating any new one.

            Extension to avoid removing timesheets
        """
        for line in self:
            timesheet_lines = line.mapped('analytic_line_ids').filtered(
                lambda l: l.employee_id and l.project_id)
            line.write({
                'analytic_line_ids': [(3, x.id) for x in timesheet_lines],
            })
            super(AccountMoveLine, line).create_analytic_lines()
            line.write({
                'analytic_line_ids': [(4, x.id) for x in timesheet_lines],
            })
