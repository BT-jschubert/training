from datetime import datetime
from datetime import timedelta

from odoo import api, fields, models

from odoo.exceptions import ValidationError

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

from odoo.tools.translate import _


class Session(models.Model):
    _name = "openacademy.session"

    name = fields.Char(required=True, string="Name")
    start_date = fields.Date(required=True, string="Start date",
                             default=fields.Date.today)
    duration = fields.Integer(required=True, string="Duration (D)")
    duration_h_comp = fields.Integer(compute='_compute_duration_h',
                                     string="Duration (h)")
    seats = fields.Integer(required=True, string="Number of seats")
    course_id = fields.Many2one('openacademy.course', 'Related course')
    instructor = fields.Many2one('res.partner', 'Instructor')
    attend_ids = fields.Many2many('res.partner', 'attend_session_rel')
    color = fields.Integer(string="Color")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done')], default='draft')

    taken_seat_per = fields.Integer(compute='_compute_taken_seat_per',
                                    string="Taken Seats")
    end_date = fields.Date(compute='_compute_end_date', string="End Date",
                           inverse='_inverse_set_end_date', store=True)
    is_full = fields.Boolean(compute='_compute_is_full', string="Full",
                             search='_search_full')
    course_description = fields.Text(related='course_id.description')

    @api.model
    def update_state_cron(self):
        sessions_to_update = self.search(['&', ('state', '=', 'confirmed'), (
            'end_date', '>', datetime.now().date())])
        for session in sessions_to_update:
            session.state = 'done'

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
                    'message': "{0} attendees already registered but only {"
                               "1} seats planned".format(
                                   len(self.attend_ids), self.seats),
                }
            }

    @api.multi
    def edit_session(self):
        return {'type': 'ir.actions.act_window',
                'res_model': 'openacademy.session',
                'view_mode': 'form',
                'res_id': self.id}

    @api.constrains('instructor', 'attend_ids')
    def _check_valid_instructor(self):
        if self.attend_ids.filtered(lambda a: a.id == self.instructor.id):
            raise ValidationError(
                _('Error ! Instructor cannot be part of the attendees'))

    @api.depends('attend_ids', 'seats')
    def _compute_taken_seat_per(self):
        for record in self:
            if len(record.attend_ids) == 0 or record.seats < 1:
                record.taken_seat_per = 0
            else:
                record.taken_seat_per = len(
                    record.attend_ids) / record.seats * 100

    @api.depends('duration')
    def _compute_duration_h(self):
        for record in self:
            record.duration_h_comp = record.duration * 24

    @api.depends('duration', 'start_date')
    def _compute_end_date(self):
        for record in self:
            record.end_date = \
                str((datetime.strptime(
                    record.start_date, DEFAULT_SERVER_DATE_FORMAT) + timedelta(
                    days=record.duration - 1)).date())

    def _inverse_set_end_date(self):
        for record in self:
            if not record.start_date or datetime.strptime(
                    record.start_date,
                    DEFAULT_SERVER_DATE_FORMAT) > datetime.strptime(
                    record.end_date, DEFAULT_SERVER_DATE_FORMAT):
                continue
            record.duration = (datetime.strptime(record.end_date,
                                                 DEFAULT_SERVER_DATE_FORMAT
                                                 ).date() - datetime.strptime(
                record.start_date, DEFAULT_SERVER_DATE_FORMAT).date()).days + 1

    def _search_full(self, operator, args=None):

        # Trick to change operator #
        search_value = True
        if operator == '!=':
            search_value = False

        records = self.search([]).filtered(lambda r: r.is_full == search_value)
        domain = [('id', 'in', records.ids)]
        return domain

    @api.one
    def change_status_confirme(self):
        self.state = 'confirmed'

    @api.one
    def change_status_draft(self):
        self.state = 'draft'

    @api.one
    def change_status_done(self):
        self.state = 'done'

    @api.depends('taken_seat_per')
    def _compute_is_full(self):
        for record in self:
            record.is_full = record.taken_seat_per == 100
