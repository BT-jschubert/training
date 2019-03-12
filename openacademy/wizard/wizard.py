from odoo import fields, models, api

class Wizard(models.TransientModel):
    _name = 'wizard'


    # @api.model #En principio no hace falta por ser una funcion interna que no usa ORM
    #def _get_default_session(self):
    #    return self.env['session'].browse(self._context.get('active_id'))

    #sessions = fields.Many2one(comodel_name='session', ondelete="set null", string="Session:",
    #                           default=_get_default_session)

    sessions = fields.Many2many(comodel_name='session', string="Sessions", required=True)

    attendees = fields.Many2many(comodel_name="res.partner", relation="wizard_attendees", column1="session_id",
                                 column2="attendee_id", string="Attendees")
                                # Note that is a different "many2many" than the one in sessions.attendees.
                                # Here is a many2many between wizard and partners
                                # in sessions.attendees is a many2many between session and partners



    @api.multi
    def add_attendees(self):
        # Using the new API
        # for ses in self.sessions:
        #     ses.attendees |= self.attendees

        # Using the old API (v10)
        for att in self.attendees:
            self.sessions.write({'attendees': [(4, att.id)]})
