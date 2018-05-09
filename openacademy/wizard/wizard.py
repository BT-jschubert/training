from odoo import fields, models

class Wizard(models.TransientModel):
    _name = 'wizard'


    def set_default_session(self):
        return self._content.get("active_id")

    sessions = fields.Many2one(comodel_name='session', ondelete="set null", string="Session:", default=set_default_session)

    partners = fields.Many2many(comodel_name="res.partner", relation="session_attendees", column1="session_id",
                                 column2="attendee_id")