from odoo import fields, models, _, api


class SessionWizard(models.Model):
    _name = "openacademy.session_wizard"

    current_session = fields.Many2one(comodel_name="openacademy.session",
                                      default=lambda self: self._context.get('active_id'))
    partners = fields.Many2many("res.partner", "session_wizard_partner_rel")

    @api.multi
    def save_data(self):
        for r in self:
            r._context.get('active_model')
