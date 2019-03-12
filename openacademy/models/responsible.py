from odoo import fields, models, _

class OpenacademyResponsible(models.Model):
    _name = 'openacademy.responsible'

    name = fields.Char(string="Responsible name", required=True)
