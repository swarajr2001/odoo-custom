# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductTemplate(models.Model):
    """inherited module sales"""
    _inherit = 'product.template'

    def action_view(self):
        """open wizard wizard_form """
        return {
            'name': "Test Wizard",
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'wizard.view',
            'view_id': self.env.ref('sales_automation.wizard_form_view').id,
            'target': 'new',
            'context': {
                'default_price': self.list_price,
                'default_product_id': self.id
            }
        }


class SaleAuto(models.TransientModel):
    """"model for wizard"""
    _name = 'wizard.view'
    _description = 'model for wizard'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer",
        required=True)
    quantity = fields.Float(string="Quantity", default="1")
    price = fields.Float(string="price")
    product_id = fields.Many2one('product.template', string="product", readonly=True)

    def action_confirm(self):
        """Create a sale order"""
        find_quotations = self.env['sale.order'].search(
            [('partner_id', '=', self.partner_id.id), ('state', '=', 'draft')], limit=1)
        products_id = self.env['product.product'].search([('product_tmpl_id.id', '=', self.product_id.id)], limit=1)
        if find_quotations:
            find_quotations.order_line = [fields.Command.create({
                    'product_id': products_id.id,
                    'name': self.product_id.name,
                    'product_uom_qty': self.quantity,
                    'price_unit': self.price,
                    'price_subtotal': self.quantity * self.price,
            })]
            find_quotations.action_confirm()
            return {
                'type': 'ir.actions.act_window',
                'name': 'Sale oder',
                'res_model': 'sale.order',
                'view_mode': 'form',
                'res_id': find_quotations.id,
                'target': 'current',
            }
        else:
            sale_order = self.env['sale.order'].create({
                    'partner_id': self.partner_id.id,
                    'order_line': [fields.Command.create({
                        'product_id': products_id.id,
                        'name': self.product_id.name,
                        'product_uom_qty': self.quantity,
                        'price_unit': self.price,
                        'price_subtotal': self.quantity * self.price,
                    })]
            })
            sale_order.action_confirm()
            return {
                'type': 'ir.actions.act_window',
                'name': 'Sale oder',
                'res_model': 'sale.order',
                'view_mode': 'form',
                'res_id': sale_order.id,
                'target': 'current',
            }



