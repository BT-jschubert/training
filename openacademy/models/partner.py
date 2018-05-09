from odoo import fields, models

class Partner(models.Model):
    _inherit="res.partner"

    instructor = fields.Boolean(string="Is an instructor", default="False")
    sessions = fields.Many2many(comodel_name="session", relation="session_attendees", column1="attendee_id",
                                 column2="session_id")