# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api

class Partner(models.Model):
    _inherit = 'res.partner'

    is_instructor = fields.Boolean(string="Is an instructor")
    sessions = fields.Many2many("sessions", "atendeed_sessions", string="Sessions attended")