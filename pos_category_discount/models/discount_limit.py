# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.tools._monkeypatches import literal_eval


class PosConfig(models.Model):
    _inherit = 'pos.config'
    product_category_ids = fields.Many2many('pos.category',
                                            'pos_category_ids', string="pos_categ_id")
    discount_limit = fields.Integer()
    is_discount = fields.Boolean()


class ResConfigSettings(models.TransientModel):
    """added discount limit many to many field in the res settings of pos"""
    _inherit = 'res.config.settings'
    is_discount = fields.Boolean(related='pos_config_id.is_discount',
                                 string="Set product category discount",
                                 readonly=False)
    product_categories_ids = fields.Many2many(related='pos_config_id.product_category_ids', string="Product "                                                                                                  "categories",
                                              readonly=False)
    discount_limit = fields.Integer(related='pos_config_id.discount_limit', string="Maximum discount", readonly=False)

    @api.onchange('is_discount', 'product_categories_ids','discount_limit', 'picking_type_id')
    def onchange_is_discount(self):
        print(self.env['pos.config'].mapped('picking_type_id'))
        if not self.is_discount:
            self.discount_limit = 0
            self.product_categories_ids = None

