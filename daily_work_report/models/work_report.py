# -*- coding: utf-8 -*-

from odoo import fields, models


class WorkReport(models.Model):
    _name = 'employee.report'
    _description = 'this models hold the data of each employee work report'

    email = fields.Char(string='Email')

