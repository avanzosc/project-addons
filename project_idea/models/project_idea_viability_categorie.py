# Copyright 2018 Gontzal Gomez - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ProjectIdeaViabilityCategorie(models.Model):
    _name = 'project.idea.viability.categorie'

    name = fields.Char(string='Name')
