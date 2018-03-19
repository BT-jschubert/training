from odoo import models,fields,_
from odoo import api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATE_FORMAT
from datetime import datetime
from datetime import timedelta

class Session(models.Model):
    _name = 'openacademy.session'
    name = fields.Text(required=True)
    start_date = fields.Datetime(default=fields.Date.today())
    duration=fields.Float()
    number_of_seats=fields.Integer()
    related_Course_id=fields.Many2one('openacademy.curso')
    instructor_id=fields.Many2one('res.partner', domain= lambda self :  self._get_instructors_and_teachers())
    attendees_ids = fields.Many2many('res.partner','session_partner_rel')
    percentage_of_seats_taken = fields.Integer(compute='_percentage_seats_taken',store=True)
    end_date=fields.Datetime(compute='_get_end_date',inverse='_set_end_date')
    course_description=fields.Text(related='related_Course_id.descripcion')

    @api.depends('number_of_seats','attendees_ids')
    def _percentage_seats_taken(self):
        for each in self:
            if each.number_of_seats != 0:
                each.percentage_of_seats_taken = len(each.attendees_ids)*100/each.number_of_seats

    @api.depends('duration','start_date')
    def _get_end_date(self):
        for each in self:
            each.end_date =  timedelta(hours=+each.duration) + datetime.strptime(each.start_date,DATE_FORMAT)
            each.end_date =  datetime.strptime(each.end_date,DATE_FORMAT)

    def _set_end_date(self):
        for each in self:
            tmp_datetime_td =  datetime.strptime(each.end_date,DATE_FORMAT) - datetime.strptime(each.start_date,DATE_FORMAT)
            each.duration = tmp_datetime_td.total_seconds()/3600

    def _get_instructors_and_teachers(self):
        teacher1_id = self.env.ref('openacademy.teacher1').id
        teacher3_id = self.env.ref('openacademy.teacher3').id
        #isinstructor_id = self.env.ref('res.partner.is_instructor')
        return ['|','|',('is_instructor',"=",True),('category_id',"=",teacher1_id),('category_id',"=",teacher3_id)]

