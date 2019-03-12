# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Course(models.Model):
    _name = 'course'
    _rec_name = 'title'

    title = fields.Char(string='Title')
    description = fields.Text(string='Description of the course')
    sessions = fields.One2many('session', 'related_course', string='Sessions')
    responsible = fields.Many2one('res.users', string='Responsible')

    _sql_constraints = [
        ('different_title_description', 'CHECK(title != description)',
         'Title and descriptions must be different'),
        ('title_unique', 'UNIQUE(title)', 'Title must be unique')
    ]
