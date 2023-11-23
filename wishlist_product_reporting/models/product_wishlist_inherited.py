# -*- coding: utf-8 -*-

from odoo import models


class ProductWishlist(models.Model):
    """this product.wishlist model is inherited to define the name_get function"""
    _inherit = 'product.wishlist'

    def name_get(self):
        result = []

        for rec in self:
            result.append((rec.id, '%s  wishlist on  %s' % (rec.partner_id.name, rec.create_date.date())))

        return result
