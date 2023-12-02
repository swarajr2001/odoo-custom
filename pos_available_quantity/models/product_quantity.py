# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProductProduct(models.Model):
    """inherited the product.Product and added pos_picking_type_id_stock"""
    _inherit = 'product.product'
    pos_stock_product_quantity = fields.Float()


class PosSession(models.Model):
    """inherited pos.session to load the custom field"""
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        """function to load pos_stock_product_quantity field to pos"""

        pos_stock = self.config_id.picking_type_id.default_location_src_id.quant_ids
        all_product = self.env['product.product'].search([])
        for rec in all_product:
            rec.pos_stock_product_quantity = 0.0
        for stock_product_id in pos_stock:
            stock_product_id.product_id.pos_stock_product_quantity = stock_product_id.quantity

        result = super()._loader_params_product_product()
        result['search_params']['fields'].append('pos_stock_product_quantity')
        return result
