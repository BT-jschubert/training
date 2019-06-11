from odoo import models, fields

class Wizard(models.TransientModel):
    _name = 'openacademy.wizard'

    sessions = fields.Many2many('openacademy.session', string="Sessions")
    attendees = fields.Many2many('res.partner', string="Attendees")

    def save_attendees(self):
        for s in self.sessions:
            s.attendees = s.attendees + self.attendees
