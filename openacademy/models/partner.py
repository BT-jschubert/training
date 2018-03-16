from odoo import fields, models, _

class OpenacademyPartner(models.Model):
    _name = 'openacademy.partner'

    name = fields.Char(string="Partner name", required=True)
