# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
from odoo import models, fields, api, _


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string='Patient')

    @api.constrains('email')
    def _check_if_email_already_exist_in_patient(self):
        patients = self.env['hms.patient'].search([('email', '=', self.email)])
        if patients:
            raise ValidationError("Email Is Already Exist in Patients Mails")

    def unlink(self):
        if self.related_patient_id:
            raise ValidationError("You Can`t Delete A Customer Related To Patient")