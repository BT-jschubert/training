# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Partner(models.Model):
    # _name = 'partner_inheritance'
    _inherit = 'res.partner'

    instructor = fields.Boolean(string='Instructor')
    sessions = fields.Many2many('session', 'partner_session_ref',
                                string='Sessions')
