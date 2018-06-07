# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class Course(models.Model):
    _name = 'course'
    _rec_name = 'title'

    title = fields.Char(string='Subject:')
    description = fields.Text(string='Description Of the subject')
    sessions = fields.One2many("sessions","related_course")
    responsible = fields.Many2one("res.users", string="Responsible")

    _sql_constraints = [('check_title_constraint', 'CHECK(title!=description)', 'The name is equal to the description'),
                        ('check_unique_title', 'UNIQUE(title)', 'The name already exists')]
