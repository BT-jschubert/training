from datetime import timedelta, datetime

from AptUrl.Helpers import _

from odoo import api, fields, models
from odoo.exceptions import ValidationError, RedirectWarning, except_orm


class Session(models.Model):
    _name = "openacademy.session"

    name = fields.Char(required=True, string="Name")
    start_date = fields.Date(required=True, string="Start date", default=fields.Date.today)
    duration = fields.Integer(required=True, string="Duration (D)")
    seats = fields.Integer(required=True, string="Number of seats")
    course_id = fields.Many2one('openacademy.course', 'Related course')
    instructor = fields.Many2one('res.partner', 'Instructor')
    attend_ids = fields.Many2many('res.partner', 'attend_session_rel')

    taken_seat_per = fields.Integer(compute='_compute_taken_seat_per', string="Taken Seats")
    end_date = fields.Date(compute='_compute_end_date', string="End Date", inverse='_set_end_date')
    is_full = fields.Boolean(compute='_compute_is_full', string="Full",search='_search_full')
    course_description = fields.Text(related='course_id.description')

    @api.onchange('seats')
    def _onchange_seats(self):

        if self.seats < 0:
            return {
                'warning': {
                    'title': "Seat errors",
                    'message': "Negative seat value",
                }
            }
        elif self.seats < len(self.attend_ids):
            return {
                'warning': {
                    'title': "Seat errors",
                    'message': "{0} attendees already registered but only {1} seats planned".format(len(self.attend_ids),self.seats),
                }
            }


    @api.constrains('instructor','attend_ids')
    def _check_valid_instructor(self):
       if self.attend_ids.filtered(lambda a: a.id == self.instructor.id ):
            raise ValidationError(_('Error ! Instructor cannot be part of the attendees'))


    @api.depends('attend_ids','seats')
    def _compute_taken_seat_per(self):
        for record in self:
            if len(record.attend_ids) == 0 or record.seats < 1:
                record.taken_seat_per = 0
            else:
                record.taken_seat_per = len(record.attend_ids)/record.seats*100

    @api.depends('duration', 'start_date')
    def _compute_end_date(self):
        for record in self:
            record.end_date = (datetime.strptime(record.start_date, '%Y-%m-%d')+timedelta(days=record.duration-1)).date()

    def _set_end_date(self):
        for record in self:
            if not (record.start_date) or datetime.strptime(record.start_date, '%Y-%m-%d') > datetime.strptime(record.end_date, '%Y-%m-%d'):
                continue
            record.duration = (datetime.strptime(record.end_date, '%Y-%m-%d').date()-datetime.strptime(record.start_date, '%Y-%m-%d').date()).days+1

    def _search_full(self, operator, args = None):

        search_value = True
        if operator == '!=':
            search_value = False

        records = self.search([]).filtered(lambda r: r.is_full == search_value)
        domain = [('id', 'in', records.ids)]
        return domain


    @api.depends('taken_seat_per')
    def _compute_is_full(self):
        for record in self:
            record.is_full = record.taken_seat_per == 100