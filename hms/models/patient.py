# -*- coding: utf-8 -*-
import datetime
import time
from odoo.exceptions import ValidationError
from odoo import models, fields, api, _
from datetime import date
from dateutil import relativedelta
import re


class hms_patient(models.Model):
    _name = 'hms.patient'
    _rec_name = 'first_name'
    _description = 'This Model Explain The Patient Status'
    _inherit = 'mail.thread'

    first_name = fields.Char(string="First Name", required=True, tracking=True)
    last_name = fields.Char(string="Last Name", required=True, tracking=True)
    bd = fields.Date(string="Birthday", tracking=True)
    history = fields.Html(string="History", tracking=True)
    cr_ratio = fields.Float(String="CR Ratio")
    blood_type = fields.Selection([('A', 'A'), ('A+', 'A+'), ('B+', 'B+'), ('AB+', 'AB+'), ('O+', 'O+'), ('O-', 'O-')],
                                  default='O+', string="Blood Type")
    pcr = fields.Boolean(string="PCR", tracking=True)
    image = fields.Image(tracking=True)
    address = fields.Text(string="Address", tracking=True)
    age = fields.Integer(string="Age", compute="_compute_age", store=True, readonly=True)
    dept_id = fields.Many2one('hms.department', string="Department", tracking=True)
    doctors = fields.Many2many('hms.doctor', string="Doctors", tracking=True)
    dept_capacity = fields.Integer(string="Department Capacity", related='dept_id.capacity')
    email = fields.Char(string="E-mail")
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], default='undetermined', string="Status", tracking=True)
    #Patient Model SQL Constrants
    _sql_constraints = [
        ('uniq_email',
         'UNIQUE (email)',
         'This Email Is Already Exist')]
    # --------------Patient Model Constraints---------------
    @api.constrains('pcr', 'bd', 'dept_id', 'email')
    def _patient_model_constrains(self):
        # cr_ratio validation
        if self.pcr:
            if self.cr_ratio == 0.0:
                raise ValidationError("CR Ratio is Mandatory")

        # age validation
        current_year = date.today().year
        current_month = date.today().month
        current_day = date.today().day
        if self.bd:
            birth_year = self.bd.year
            birth_month = self.bd.month
            birth_day = self.bd.day
            if current_year < birth_year:
                raise ValidationError("Enter A correct birthday")
            elif not current_year > birth_year:
                if current_month < birth_month:
                    raise ValidationError("Enter A correct birthday")
                elif not current_month > birth_month:
                    if current_day < birth_day:
                        raise ValidationError("Enter A correct birthday")

        # check if department is opened
        if self.dept_id:
            if not self.dept_id.is_opened:
                raise ValidationError("You can`t choose closed department")

        # check email expression
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match == None:
                raise ValidationError('Not a valid E-mail ID')


    def action_undetermined(self):
        self.state = "undetermined"

    def action_good(self):
        self.state = "good"

    def action_fair(self):
        self.state = "fair"

    def action_serious(self):
        self.state = "serious"

    def name_get(self):
        res = []
        for record in self:
            name = record.last_name
            if record.first_name:
                name = record.first_name + ' ' + name
            res.append((record.id, name))
        return res

    @api.depends('bd')
    def _compute_age(self):
        for rec in self:
            current_year = date.today().year
            current_month = date.today().month
            current_day = date.today().day
            if rec.bd:
                birth_year = rec.bd.year
                print(birth_year)
                rec.age = current_year - birth_year

    # def _inverse_compute_age(self):
    #     for rec in self:
    #         today = date.today()
    #         rec.bd = today - relativedelta.relativedelta(years=rec.age)

    # if rec.bd:
    #     day = rec.bd+relativedelta.relativedelta(years=rec.age)
    #     rec.bd = day - relativedelta.relativedelta(years=rec.age)
    # else:
    #     today = date.today()
    #     rec.bd = today - relativedelta.relativedelta(years=rec.age)

    @api.onchange('age')
    def _check_age_value(self):
        if self.age:
            if self.age < 30:
                self.pcr = True
                return {
                    'domain': {'age': [('age', '&lt;', 30)]},
                    'warning': {'title': "Warning",
                                'message': "PCR is checked automatically"}
                }
            else:
                self.pcr = False
