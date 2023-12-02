# -*- coding: utf-8 -*-

from odoo import fields, models


class ComboConfiguration(models.Model):
    _name = 'combo.configuration'
    _description = 'this model represents the configuration of the product'

    combo_pos_category_id = fields.Many2one('pos.category', string='Pos category', help='pos category selection field')
    combo_product_ids = fields.Many2many('product.product', string='Combo products',
                                         domain="[('pos_categ_id', '=', combo_pos_category_id)]",
                                         help='choose specific product')
    is_required_product = fields.Boolean(string='Is required', help='weather this product is a required one')
    item_count = fields.Integer(string='Item count', help='Item count of the selected products')
    product_template_id = fields.Many2one('product.product')



