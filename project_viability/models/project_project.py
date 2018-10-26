# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class ProjectProject(models.Model):
    _inherit = 'project.project'

    def _default_viability_templ_id(self):
        get_param = self.env['ir.config_parameter'].sudo().get_param
        default_tmpl_id = int(
            get_param('project_viability.viability_templ_id'))
        return self.env['project.viability.template'].browse(default_tmpl_id)

    viability_templ_id = fields.Many2one(
        comodel_name='project.viability.template', string='Viability Template',
        default=_default_viability_templ_id)
    viability_line_ids = fields.One2many(
        comodel_name='project.viability.line', inverse_name='project_id',
        string='Viability Lines')
    viability_categ_line_ids = fields.One2many(
        comodel_name='project.viability.category.line',
        inverse_name='project_id', string='Viability Category Lines')
    viability_score = fields.Float(
        string='Score', compute='_compute_viability_score',
        digits=dp.get_precision('Viability Score'))
    viability_decision_id = fields.Many2one(
        comodel_name='project.viability.decision', string='Decision')
    viability_comments = fields.Text(string='Comments')

    @api.model
    def create(self, values):
        res = super(ProjectProject, self).create(values)
        res._reload_viability_categ_line_ids()
        res.button_apply_viability_template()
        return res

    @api.multi
    def write(self, values):
        res = super(ProjectProject, self).write(values)
        if 'viability_line_ids' in values:
            self._reload_viability_categ_line_ids()
        return res

    @api.multi
    def button_apply_viability_template(self):
        for project in self.filtered('viability_templ_id'):
            project.viability_line_ids.unlink()
            project.viability_line_ids = [
                (0, 0, {'factor_id': x.id})
                for x in project.mapped('viability_templ_id.factor_ids')]

    @api.multi
    def _reload_viability_categ_line_ids(self):
        for project in self:
            project.viability_categ_line_ids.unlink()
            project.viability_categ_line_ids = [
                (0, 0, {'categ_id': x.id})
                for x in project.mapped('viability_line_ids.categ_id')]

    @api.depends('viability_categ_line_ids',
                 'viability_categ_line_ids.weighted_score')
    def _compute_viability_score(self):
        for project in self:
            project.viability_score = sum(
                project.mapped('viability_categ_line_ids.weighted_score'))


class ProjectViabilityDecision(models.Model):
    _name = 'project.viability.decision'
    _description = 'Viability Decision'

    name = fields.Char(string='Name', required=True, translate=True)
