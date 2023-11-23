# -*- coding: utf-8 -*-
from odoo import fields, models


class BrandField(models.Model):
    """inherited product.product model to add new field brand """
    _inherit = 'product.product'
    brand = fields.Char(string="Brand")


class PosSession(models.Model):
    """inherited pos.session to load the fields from product.product"""
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        """function to load field to pos"""
        result = super()._loader_params_product_product()
        result['search_params']['fields'].extend(['brand'])
        return result
