from odoo import fields, models


class Wizard(models.TransientModel):
    _name = 'openacademy.wizard'

    session_ids = fields.Many2many('openacademy.session', 'wizard_session')
    partner_ids = fields.Many2many('res.partner', 'partner_session_rel')

    def save_attendees(self):
        for wizard in self:
            for session in wizard.session_ids:
                for attendee in wizard.partner_ids:
                    if attendee not in session.attend_ids:
                        session.attend_ids = (4, attendee.id)
