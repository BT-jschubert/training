from odoo import fields, models, api, _
from datetime import date, datetime, timedelta

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT

class Session(models.Model):
    _name = 'session'
    _rec_name = 'name'

    #####################
    #General methods
    #####################
    def domain_def(self):
        #This 'if' avoids a problem in the module installation, since the files .py are processed before than .xml ones,
        #and the constaint defined points to an element inside 'demo_data.xml'
        if(self.env['ir.model.data'].search(['&',('module', '=', 'openacademy'), ('name','=','teacher'),('model','=','res.partner.category')])):
            # The ref is the id in the xml demo data. It won't work if
            # record is created "by hand" in the web
            return ['|', ('instructor', '=', True), ('category_id', 'child_of', self.env.ref("openacademy.teacher").id)]




    #####################
    #Fields
    #####################
    name = fields.Char(string='Session name:')
    start_date = fields.Date(string="Start date:", default=fields.Date.today())
    duration = fields.Float(string='Duration in days:')
    end_date = fields.Date(string="End date:", compute = "_get_end_date", inverse="_set_end_date", store = True)
    num_seats = fields.Integer(string = 'Number of seats', default=1)
    taken_seats_percent = fields.Float(string="Percentage of taken seats:", compute="_get_percent")

    course_id = fields.Many2one(comodel_name='course', ondelete="set null", string="Related course:", required=True)
    course_description = fields.Text(related='course_id.description', string="Course description:")
    instructor_id = fields.Many2one(comodel_name='res.partner', ondelete="set null", domain=domain_def, string="Instructor:")

    attendees = fields.Many2many(comodel_name="res.partner", relation="session_attendees", column1="session_id", column2="attendee_id")
    num_attendees = fields.Integer(string="Number of attendees", compute='_get_num_attendees', store=True)

    color = fields.Integer(string="Color:")

    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done')], default="draft")

    duration_hours = fields.Integer(string="Duration in hours:", compute="_get_duration_hours")

    #####################
    #Methods for computed fields
    #####################
    @api.depends('num_seats', 'attendees')
    def _get_percent(self):
        for r in self:
            if not (r.num_seats):
                continue
            num_attendees = len(r.attendees)
            r.taken_seats_percent = num_attendees / r.num_seats * 100.0

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            s_date = datetime.strptime(r.start_date, DATE_FORMAT)
            e_date = s_date + timedelta(days=int(r.duration))
            r.end_date = e_date.strftime(DATE_FORMAT)

    @api.depends('duration')
    def _get_duration_hours(self):
        for r in self:
            r.duration_hours = r.duration * 24

    @api.depends('attendees')
    def _get_num_attendees(self):
        for r in self:
            r.num_attendees = len(r.attendees)

    #####################
    # Methods for inverse fields
    #####################
    def _set_end_date(self):
        for r in self:
            if not r.end_date or not r.start_date:
                continue
            s_date = datetime.strptime(r.start_date, DATE_FORMAT)
            e_date = datetime.strptime(r.end_date, DATE_FORMAT)

            res = e_date - s_date
            r.duration = res.days

    #####################
    # Methods for "onchange"
    #####################
    @api.onchange('num_seats')
    def _onchange_seats(self):
        if self.num_seats <= 0:
            return {
                'warning': {
                    'title': "Incorrect number of seats",
                    'message': "Number of seats must be a positive number",
                }
            }
        elif self.num_seats < len(self.attendees):
            return {
                'warning': {
                    'title': "Incorrect number of seats",
                    'message': "There are more participants than seats! Number of seats must be higher than number of attendees",
                }
            }

    ################################
    #Methods for Python constraints
    ################################
    @api.constrains('instructor_id', 'attendees')
    def _instructor_not_attendee(self):
        for r in self:
            if r.instructor_id in r.attendees:
                raise Exception(_("An instructor you have chosen is an attendee. Would you like to continue?"))

    #############################
    # Methods for button actions
    #############################
    @api.multi
    def view_action(self):
        return{
            'type': 'ir.actions.act_window',
            'res_model': 'session',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('openacademy.session_form').id,
            'target': 'current'
        }

    @api.multi
    def confirm_action(self):
        for r in self:
            r.state ='confirmed'

    @api.multi
    def reedit_action(self):
        for r in self:
            r.state = 'draft'

    @api.multi
    def finish_action(self):
        for r in self:
            r.state = 'done'

    #########################
    #Methods for schedulers
    #########################
    @api.model
    def cron_confirmed2done(self):
        records = self.search(['&', ('end_date', '<', date.today()), ('state', '=', 'confirmed')])
        for r in records:
            r.state = 'done'
