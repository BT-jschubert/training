from odoo import fields, models

class Session(models.Model):
    _name = 'session'
    _rec_name = 'name'

    name = fields.Char(string='Session name:')
    start_date = fields.Date(string="Start date:", default=fields.Date.today())
    duration = fields.Float(string='Duration in hours:')
    num_seats = fields.Integer(string = 'Number of seats')

    course_id = fields.Many2one(comodel_name='course', ondelete="set null", string="Related course:", required="True")
    instructor_id = fields.Many2one(comodel_name='res.partner', ondelete="set null", string="Instructor:")
    responsible_id = fields.Many2one(comodel_name='res.users', ondelete="set null", string="Responsible:")
    attendees = fields.Many2many(comodel_name="res.partner", relation="session_attendees", column1="session_id", column2="attendee_id")