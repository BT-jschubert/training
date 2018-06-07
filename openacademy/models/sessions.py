# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api
from datetime import datetime,timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo import _


class Sessions(models.Model):
    _name = 'sessions'

    name = fields.Char(string='Name:')
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Integer(string="Duration:")
    number_of_seats = fields.Integer(string="Number of seats:")
    taken_seats_percent = fields.Float(string="taken seats perfent", compute='_calculate_taken_seats') #by default: store=False
    end_date = fields.Date(string="end date", store=False, compute='_calculate_end_date', inverse='_set_start_date')
    related_course = fields.Many2one("course")
    # instructor = fields.Many2one("res.partner")
    instructor = fields.Many2one("res.partner", string="Instructor", domain = [("is_instructor","=",True)])
    attendees = fields.Many2many("res.partner","attendees",string="attendees")
    course_description = fields.Text(related='related_course.description', string="Related Course:") #Related fields must not be stored: store=True
    color = fields.Integer(string="Color")
    hours_duration = fields.Integer(string="hours_duration", store=True, compute='_calculate_duration_in_hours')
    number_of_attendees = fields.Integer(string="Number of Attendees", store=True, compute='_calculate_number_of_attendees')
    state = fields.Selection([('draft','DRAFT'), ('confirmed','CONFIRMED'), ('done','DONE')], default='draft')

    @api.depends('number_of_seats','attendees')
    def _calculate_taken_seats(self):
        for record in self:
            if not (record.number_of_seats):
                continue
            record.taken_seats_percent = len(record.attendees) / record.number_of_seats * 100.0

    @api.depends('attendees')
    def _calculate_number_of_attendees(self):
        for record in self:
            record.number_of_attendees = len(record.attendees)

    @api.depends('duration')
    def _calculate_duration_in_hours(self):
        for record in self:
            record.hours_duration = record.duration * 24

    @api.depends('start_date','duration')
    def _calculate_end_date(self):
        for record in self:
            duration = record.duration
            update_days = timedelta(days=duration)

            datetime_object = datetime.strptime(record.start_date, DATE_FORMAT)
            datetime_object = datetime_object + update_days

            record.end_date = datetime_object.strftime(DATE_FORMAT)

    def _set_start_date(self):
        for record in self:
            if(record.duration != None & record.end_date != None):
                duration = record.duration
                update_days = timedelta(days=duration)
                datetime_object = datetime.strptime(record.end_date, DATE_FORMAT)
                record.start_date = datetime_object - update_days

    def print_maximun_attendees_warning_message(self):
        return {
                'warning': {
                    'title': _("Maximun number of attendees reached."),
                    'message': "The maximun number of attendees have been reached. No more can be assigned."
                }
            }

    @api.onchange('number_of_seats')
    def _onchange_number_of_seats(self):
        if self.number_of_seats < 0:
            return {
                'warning': {
                    'title': _("Number of seats invalid"),
                    'message': "A negative value can not be set for the number of seats. "
                               "System will set it to zero by default."
                }
            }

        elif self.number_of_seats < len(self.attendees):
            return self.print_maximun_attendees_warning_message()

    @api.onchange('attendees')
    def _onchange_maximun_participants(self):
        if self.number_of_seats < len(self.attendees):
            return self.print_maximun_attendees_warning_message()

    @api.constrains('attendees')
    def _instructor_not_present(self):
        if len(self.attendees) > 0 and self.instructor != None and self.instructor in self.attendees:
            raise Exception("The instructor of the seasson can not be set in the attendees of the session.")

    @api.multi
    def open_record(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sessions',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('openacademy.session_form_view').id,
            'target': 'current',
        }

    #FUNCTIONS FOR THE WORKFLOW STAGES CONTROL.
    def change_to_draft(self):
        self.state = 'draft'

    def change_to_confirmed(self):
        self.state = 'confirmed'

    def change_to_done(self):
        self.state = 'done'

    #CRON FUNCTION.
    @api.model
    def cron_done(self):
        sessions_table = self.env['sessions']

        today = datetime(datetime.now(), DATE_FORMAT)
        for session in sessions_table.search([{('state','=','confirmed'),('end_date','<',today)}]):
            session.state = 'done'

