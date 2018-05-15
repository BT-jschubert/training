from odoo import fields, models, api

class Wizard(models.TransientModel):
    _name = 'wizard'


    @api.model
    def _get_default_session(self):
        return self.env['session'].browse(self._context.get('active_id'))

    #sessions = fields.Many2one(comodel_name='session', ondelete="set null", string="Session:",
    #                           default=_get_default_session)

    sessions = fields.Many2many(comodel_name='session', string="Sessions", required=True)

    attendees = fields.Many2many(comodel_name="res.partner", relation="wizard_attendees", column1="session_id",
                                 column2="attendee_id", string="Attendees")
                                # Note that is a different "many2many" than the one in sessions.attendees



    @api.multi
    def add_attendees(self):
        for ses in self.sessions:
            ses.attendees |= self.attendees

        # Old API (v10), but I didn't get it work
        # for record in self.attendees:
        #     self.sessions.attendees.write({(4, record.id)})