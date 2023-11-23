# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import fields, models


class FleetVehicle(models.Model):
    """inherited module fleet and custom field registration_date"""
    _inherit = 'fleet.vehicle'

    registration_date = fields.Date(string="Registration date", default=datetime.today())
