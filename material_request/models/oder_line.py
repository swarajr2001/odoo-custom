# -*- coding: utf-8 -*-
from odoo import fields, models


class OderLine(models.Model):
    _name = 'oder.line'
    _description = 'this is the model for the oder line'

    material_id = fields.Many2one('product.product', required=True)
    material_req_id = fields.Many2one('material.request')
    source_location_id = fields.Many2one("stock.location", string="Source location")
    destination_location_id = fields.Many2one("stock.location", string="Destination location")
    method = fields.Selection(string="Method",
                              selection=[
                                  ('purchase', 'Purchase'),
                                  ('internal_transfer', 'Internal transfer')
                              ], default='purchase')

