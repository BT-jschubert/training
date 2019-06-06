from odoo import models
from odoo import fields

class Wizard(models.TransientModel):
    _name = 'openacademy.wizard'

    session = fields.Many2one('openacademy.session', string="Session", required=True, default=lambda self: self._context.get('active_id'))
    attendees = fields.Many2many('res.partner', string="Attendees")

    def save_attendees(self):
        self.session.attendees = self.session.attendees + self.attendees
