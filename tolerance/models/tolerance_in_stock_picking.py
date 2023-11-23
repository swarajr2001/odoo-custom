# -*- coding: utf-8 -*-
from odoo import fields, models


class StockTolerance(models.Model):
    _inherit = "stock.move"

    tolerance_stock = fields.Integer("Tolerance",
                                     related="sale_line_id.tolerance_sale")

