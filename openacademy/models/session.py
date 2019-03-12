# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT

from odoo import _
from odoo import fields, models, api


class Session(models.Model):
    _name = 'session'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    start_date = fields.Date(string='Start date', default=fields.Date.today)
    duration = fields.Integer(string='Duration', default=5)
    number_of_seats = fields.Integer(string='Number of seats')
    related_course = fields.Many2one('course', string='Course')
    instructor = fields.Many2one('res.partner', string='Instructor',
                                 domain=[('instructor', '=', True)])
    attendees = fields.Many2many('res.partner', 'partner_session_ref',
                                 string='Attendees')
    taken_seats = fields.Float(compute='_apply_taken_seats',
                               string='Taken seats')
    end_date = fields.Date(string='End Date', compute='_apply_end_date',
                           inverse='_set_duration', store=True)
    course_description = fields.Text(related='related_course.description',
                                     store=False, string='Course description')
    color = fields.Integer(string="Color")
    duration_hours = fields.Integer(string="Duration in hours",
                                    compute="_get_duration_in_hours",
                                    store=True)
    num_attendees = fields.Integer(string="Number of attendees",
                                   compute="_get_num_attendees", store=True)
    state = fields.Selection(string="State",
                             selection=[('draft', 'Draft'),
                                        ('confirmed', 'Confirmed'),
                                        ('done', 'Done')],
                             default='draft')

    @api.depends('number_of_seats', 'attendees')
    def _apply_taken_seats(self):
        for rec in self:
            if len(rec.attendees) > 0 and rec.number_of_seats > 0:
                rec.taken_seats = len(
                    rec.attendees) * 100 / rec.number_of_seats
            else:
                rec.taken_seats = 0

    @api.depends('start_date', 'taken_seats')
    def _apply_end_date(self):
        for rec in self:
            duration = rec.duration
            update_days = timedelta(days=duration)

            datetime_object = datetime.strptime(rec.start_date, DATE_FORMAT)
            datetime_object = datetime_object + update_days

            rec.end_date = datetime_object.strftime(DATE_FORMAT)

    def _set_duration(self):
        for rec in self:
            if rec.end_date and rec.start_date:
                end_date_object = datetime.strptime(rec.end_date, DATE_FORMAT)
                start_date_object = datetime.strptime(rec.start_date,
                                                      DATE_FORMAT)
                duration = end_date_object - start_date_object
                rec.duration = duration.days

    @api.onchange('number_of_seats')
    def _on_change_taken_seats(self):
        if self.number_of_seats < 0:
            return {
                'warning': {
                    'title': _("Wrong number of seats"),
                    'message': _("Number of seats should not be negative!"),
                }
            }

    @api.onchange('attendees', 'number_of_seats')
    def _on_change_attendees(self):
        if len(self.attendees) > self.number_of_seats:
            return {
                'warning': {
                    'title': _("Too many attendees"),
                    'message': _(
                        "There are more attendees than number of seats, try to increase them"),
                }
            }

    @api.constrains('attendees')
    def __on_attendee_added(self):
        for attendee in self.attendees:
            if attendee.instructor:
                raise Exception(_('Attendee is an instructor'),
                                _('The instructor can not be an attendee!'))

    @api.constrains('instructor')
    def __on_attendee_added(self):
        if self.instructor in self.attendees:
            raise Exception(_('Instructor invalid'),
                            _('The instructor can not be also an attendee!'))

    @api.multi
    def open_session_form(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'session',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('openacademy.session_form_view').id,
            'context': {},
            'target': 'current'
        }

    @api.depends('duration')
    def _get_duration_in_hours(self):
        for rec in self:
            rec.duration_hours = rec.duration * 24

    @api.depends('attendees')
    def _get_num_attendees(self):
        for rec in self:
            rec.num_attendees = len(rec.attendees)

    @api.multi
    def state_to_confirmed(self):
        self.state = "confirmed"

    @api.multi
    def state_to_draft(self):
        self.state = "draft"

    @api.multi
    def state_to_done(self):
        self.state = "done"

    @api.model
    def to_confirm(self):
        sessions = self.search(
            [('state', '=', 'confirmed'), ('end_date', '<=', datetime.now())])

        for rec in sessions:
            rec.state = "done"
