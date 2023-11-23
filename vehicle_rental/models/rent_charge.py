# -*- coding: utf-8 -*-
from odoo import fields, models


class RentCharge(models.Model):
    """"model for rent charges"""
    _name = 'rent.charge'
    _rec_name = 'time'
    _description = 'model for rent charge'

    time = fields.Selection(selection=[('hour', 'Hour'),
                                       ('day', 'Day'),
                                       ('week', 'Week'),
                                       ('month', 'Month')], string="Time")
    amount = fields.Float(string="Amount", store=True)
    vehicle_details_id = fields.Many2one("vehicle.details", string="Vehicle")

    _sql_constraints = [('unique_time',
                         'UNIQUE(time,vehicle_details_id)',
                         "The value has been already assigned!"),
                        ]
