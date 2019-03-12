from odoo import models,fields,_
from odoo import api

class PartnerExtended(models.Model):

    _inherit = 'res.partner'
    is_instructor = fields.Boolean()
    relation_ids = fields.Many2many('openacademy.session','session_partner_rel')