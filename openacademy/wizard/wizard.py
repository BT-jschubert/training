# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api


class Wizard(models.TransientModel):
    _name = 'wizard'

    # @api.model
    # def _get_default_session(self):
    #     return self._context.get('active_id')

    # session = fields.Many2one("sessions", default=_get_default_session)
    # session = fields.Many2one("sessions", string="Session")
    sessions = fields.Many2many("sessions", "wizard_session", string="Sessions")
    attendees = fields.Many2many("res.partner", "wizard_attendees", string="Attendees")

    #TODO: CHECK IF THE ATTENDEES EXCEES THE MAXIM SEATS.
    def add_attendees(self):
        # self.session.attendees |= self.attendees #<--- ONE SESSION FOR ATTENDEES.
        for record in self.sessions:
            record.attendees |= self.attendees
            # record.attendees.write({'attendees': record.id})  #<--- OLD API

