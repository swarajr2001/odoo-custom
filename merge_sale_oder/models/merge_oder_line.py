# -*- coding: utf-8 -*-
from odoo import models, api


class MergeOderLine(models.Model):
    """inherited module sales"""
    _inherit = 'sale.order'

    def action_merge(self):
        for line in self.order_line:
            if line.id in self.order_line.ids:
                line_ids = self.order_line.filtered(
                    lambda m: m.product_id.id == line.product_id.id and m.price_unit == line.price_unit)
                quantity = sum(line.product_uom_qty for line in line_ids)
                line_ids[0].write({'product_uom_qty': quantity,
                                   'order_id': line_ids[0].order_id.id,
                                   'price_unit': line.price_unit})

                line_ids[1:].unlink() if line_ids[1:] else print("")

    def action_confirm(self):
        """Update the sales module confirm"""
        self.action_merge()
        super().action_confirm()
        print(self.env['sale.order'].search([]).sorted(lambda l: l.partner_id.name))
        a = self.env['sale.order'].search([]).sorted(lambda l: l.partner_id.id)
        print(a.search_count([('partner_id', '=', self.partner_id.id)]))

    @api.model
    def create(self, vals):
        """function of save icon"""
        res = super(MergeOderLine, self).create(vals)
        res.action_merge()
        return res
