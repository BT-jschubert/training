from odoo import models,fields,_
from odoo import api

class Wizardo(models.TransientModel):
    _name='openacademy.wizard'

    # session_relation=fields.Many2one('openacademy.session', default=lambda self: self._context.get('active_id'))
    session_relations=fields.Many2many('openacademy.session', 'wizard_session_rel',default=lambda self: self._context.get('active_ids'))
    partner_relation=fields.Many2many('res.partner','wizard_partner_rel')

    @api.multi
    def add2session(self):
        #solution with old API
        #ids_attendess=[(4, x.id) for x in self.partner_relation]
        #self.session_relation.write({'attendees_ids': ids_attendess})
        self.session_relations.attendees_ids |= self.partner_relation

    def add2sessions(self):
        #solution with old API
        #ids_attendess=[(4, x.id) for x in self.partner_relation]
        #self.session_relation.write({'attendees_ids': ids_attendess})
        for each_session in self.session_relations:
            each_session.attendees_ids |= self.partner_relation
