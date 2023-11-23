# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ToleranceInLine(models.Model):
    _inherit = 'sale.order.line'

    tolerance_sale = fields.Integer(string="Tolerance", compute='_compute_tolerance', inverse='_tolerance_inverse',
                                    store=True)

    @api.depends('order_id.partner_id.tolerance')
    def _compute_tolerance(self):
        """function to assign the tolerance value to sale.order.line tolerance field"""
        for line in self:
            if line.order_id.partner_id:
                line.tolerance_sale = line.order_id.partner_id.tolerance

    def _tolerance_inverse(self):
        """inverse function to make the compute field editable"""
        pass
