#-*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
from odoo import models, fields, api, _

class hms_department(models.Model):
    _name = 'hms.department'
    _description = 'This Model Shows Departments Data'

    name = fields.Char(string="Department Name", required=True)
    capacity = fields.Integer(string="Capacity")
    is_opened = fields.Boolean(string="Opened")
    patients_ids = fields.One2many('hms.patient','dept_id', string="Patients")
