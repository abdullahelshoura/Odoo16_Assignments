#-*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
from odoo import models, fields, api, _

class hms_doctor(models.Model):
    _name = 'hms.doctor'
    _rec_name = 'first_name'
    _description = 'This Model Show Doctors Data'

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    image = fields.Image()

    def name_get(self):
        res = []
        for record in self:
            name = record.last_name
            if record.first_name:
                name = record.first_name + ' ' + name
            res.append((record.id, name))
        return res
