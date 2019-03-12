from odoo import fields, models, api


class AddSessionsWizard(models.TransientModel):
    _name = 'add_sessions_wizard'
    _rec_name = 'wizard_session'

    def get_default_session(self):
        return self._context.get('active_id')

    wizard_session = fields.Many2one('session', string='Session')
    wizard_session_rel = fields.Many2many('session', 'wizard_session_ref',
                                          string='Sessions')
    wizard_session_attendees = fields.Many2many('res.partner',
                                                'wizard_partners_ref',
                                                string="Attendees")

    @api.multi
    def save_results_v10(self):
        attendees_id = []
        for new_attendee in self.wizard_session_attendees:
            attendees_id.append(new_attendee.id)

        self.wizard_session.attendees.write({(6, 0, attendees_id)})

    @api.multi
    def save_results(self):

        session_ids = self._context.get('active_ids')
        selected_sessions = self.env['session'].search(
            [('id', 'in', session_ids)])

        for session in selected_sessions:
            for new_attendee in self.wizard_session_attendees:
                session.attendees |= new_attendee
