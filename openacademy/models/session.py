from odoo import models, fields, _
from odoo import api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATE_FORMAT
from datetime import datetime
from datetime import timedelta
from odoo.exceptions import ValidationError


class Session(models.Model):
    _name = 'openacademy.session'
    name = fields.Text(required=True)
    start_date = fields.Datetime(default=fields.Date.today())
    duration = fields.Float()
    number_of_seats = fields.Integer(default='1')
    related_Course_id = fields.Many2one('openacademy.curso')
    instructor_id = fields.Many2one('res.partner', domain=lambda self: self._get_instructors_and_teachers())
    attendees_ids = fields.Many2many('res.partner', 'session_partner_rel')
    percentage_of_seats_taken = fields.Integer(compute='_percentage_seats_taken')
    end_date = fields.Datetime(compute='_get_end_date', inverse='_set_end_date')
    course_description = fields.Text(related='related_Course_id.descripcion')
    color = fields.Integer()
    n_of_attendees = fields.Integer(compute='_get_n_of_attendees', store=True)
    # duration_hours=fields.Integer(compute='_get_hours')
    state = fields.Selection(selection=[('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done')],
                             default='draft')

    @api.depends('number_of_seats', 'attendees_ids')
    def _percentage_seats_taken(self):
        for each in self:
            if len(each.attendees_ids) != 0:
                each.percentage_of_seats_taken = len(each.attendees_ids) * 100 / each.number_of_seats
            else:
                each.percentage_of_seats_taken = 0

    @api.depends('duration', 'start_date')
    def _get_end_date(self):
        for each in self:
            each.end_date = timedelta(hours=+each.duration) + datetime.strptime(each.start_date, DATE_FORMAT)
            each.end_date = datetime.strptime(each.end_date, DATE_FORMAT)

    def _set_end_date(self):
        for each in self:
            tmp_datetime_td = datetime.strptime(each.end_date, DATE_FORMAT) - datetime.strptime(each.start_date,
                                                                                                DATE_FORMAT)
            each.duration = tmp_datetime_td.total_seconds() / 3600

    def _get_instructors_and_teachers(self):
        teacher1_id = self.env.ref('openacademy.teacher1').id
        teacher3_id = self.env.ref('openacademy.teacher3').id
        # isinstructor_id = self.env.ref('res.partner.is_instructor')
        return ['|', '|', ('is_instructor', "=", True), ('category_id', "=", teacher1_id),
                ('category_id', "=", teacher3_id)]

    @api.onchange('number_of_seats', 'attendees_ids')
    def _check_number_of_seats(self):
        if self.number_of_seats < 0:
            return {
                'warning': {
                    'title': _('error in number of seats'),
                    'message': _('The number of seats for a session cant be negative')
                }
            }
        elif self.number_of_seats < len(self.attendees_ids):
            return {
                'warning': {
                    'title': _('error in number of seats'),
                    'message': _('The number of seats for a session cant be smaller than the number of attendees')
                }
            }
        else:
            return

    @api.constrains('instructor_id', 'attendees_ids')
    def _check_if_instructor_is_attendee(self):
        if self.instructor_id in self.attendees_ids:
            raise ValidationError(_('Error! The Instructor cant be an attendee'))
        else:
            return

    @api.multi
    def launch_formview(self):
        form_id = self.env.ref('openacademy.viewSession2').id
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_id': form_id,
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'context': {}
        }

    # def _get_hours(self):
    #     for each in self:
    #         tmp_datetime_td =  datetime.strptime(each.end_date,DATE_FORMAT) - datetime.strptime(each.start_date,DATE_FORMAT)
    #         each.duration = tmp_datetime_td.total_seconds()/3600

    @api.depends('attendees_ids', 'number_of_seats')
    def _get_n_of_attendees(self):
        for each in self:
            each.n_of_attendees = len(each.attendees_ids)

    @api.multi
    def advance_status(self):
        if self.state == 'draft':
            self.state = 'confirmed'
        elif self.state == 'confirmed':
            self.state = 'done'
        else:
            self.state = 'draft'
        # else:
        #     self.status_selection = 'done'

    @api.model
    def check_if_done(self):
       for each in self.search([]):
            if each.state == 'confirmed' and each.end_date < fields.Date.today():
                each.state = 'done'

