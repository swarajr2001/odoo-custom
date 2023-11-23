# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SalesOrder(models.Model):
    """inherited sale.order to add new field given_discount"""
    _inherit = 'sale.order'

    given_discount = fields.Float(string="Discount amount", default=0.0)
    split_amount = fields.Float(string='Split Discount', store=True)

    @api.onchange('order_line', 'given_discount')
    def change_orderline_given_discount(self):
        if self.order_line:
            total_product_quantity = sum(self.order_line.mapped('product_uom_qty'))
            self.split_amount = self.given_discount / total_product_quantity
            for val in self.order_line:
                amount = self.split_amount * val.product_uom_qty
                val.discount_amount = amount

    @api.depends('order_line.tax_id', 'order_line.price_unit', 'amount_total', 'amount_untaxed', 'currency_id')
    def _compute_tax_totals(self):
        for order in self:
            order_lines = order.order_line.filtered(lambda x: not x.display_type)
            order.tax_totals = self.env['account.tax']._prepare_tax_totals(
                [x._convert_to_tax_base_line_dict() for x in order_lines],
                order.currency_id or order.company_id.currency_id,
            )
            total = sum(order.order_line.mapped('price_subtotal'))
            order.tax_totals['amount_untaxed'] = total


class SaleOrderLine(models.Model):
    """inherited sale.order.line to add new field discount"""
    _inherit = 'sale.order.line'

    discount_amount = fields.Float(string="Discount")
    price_subtotal = fields.Monetary(
        string="Subtotal",
        compute='_compute_amount',
        store=True, precompute=True)

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'discount_amount')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            tax_results = self.env['account.tax']._compute_taxes([line._convert_to_tax_base_line_dict()])
            totals = list(tax_results['totals'].values())[0]
            amount_untaxed = totals['amount_untaxed']
            amount_tax = totals['amount_tax']
            if amount_untaxed - line.discount_amount < 0:
                line.update({
                    'price_subtotal': 0,
                    'price_tax': amount_tax,
                    'price_total': amount_untaxed + amount_tax,
                })
            else:
                line.update({
                    'price_subtotal': amount_untaxed - line.discount_amount,
                    'price_tax': amount_tax,
                    'price_total': amount_untaxed + amount_tax,
                })
