# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProjectViabilityFactor(models.Model):
    _name = 'project.viability.factor'
    _description = 'Viability Factor'
    _order = 'categ_id, code, name'

    code = fields.Char(string='Code')
    name = fields.Char(string='Name', required=True, translate=True)
    categ_id = fields.Many2one(
        comodel_name='project.viability.category', string='Category',
        required=True)

    @api.multi
    def name_get(self):
        """ name_get() -> [(id, name), ...]

        Returns a textual representation for the records in ``self``.
        By default this is the value of the ``display_name`` field.

        :return: list of pairs ``(id, text_repr)`` for each records
        :rtype: list(tuple)
        """
        result = []
        for record in self:
            result.append(
                (record.id,
                 '[{}-{}] {}'.format(record.categ_id.code, record.code,
                                     record.name)))
        return result
