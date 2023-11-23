# -*- coding: utf-8 -*-
from odoo import fields, models


class CustomerAdd(models.Model):
    _inherit = 'res.partner'
    tolerance = fields.Integer(string="Tolerance")
