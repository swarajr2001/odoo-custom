# -*- coding: utf-8 -*-
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self, val=False):
        """inherited button from stock.picking model this function checks the tolerance condition"""
        if val:
            return super().button_validate()
        else:
            for record in self.move_ids_without_package:
                if (record.quantity_done > record.tolerance_stock + record.product_uom_qty or
                        record.quantity_done < abs(record.tolerance_stock - record.product_uom_qty)):
                    return {
                        'name': "Tolerance alert",
                        'type': 'ir.actions.act_window',
                        'view_type': 'form',
                        'view_mode': 'form',
                        'res_model': 'picking.wizard',
                        'view_id': self.env.ref('tolerance.wizard_form_view').id,
                        'target': 'new',
                        'context': {
                            'default_tolerance': record.tolerance_stock,
                            'default_stock_picking_id': self.id,
                        }
                    }

            return super().button_validate()


class PickingWizard(models.TransientModel):
    """model for wizard"""
    _name = 'picking.wizard'
    _description = 'model for wizard'

    alert = fields.Text(string='Alert', default="Your demand  should satisfy the tolerance range",
                        readonly=True)
    tolerance = fields.Integer(string="Your tolerance", readonly=True)
    stock_picking_id = fields.Many2one("stock.picking", string="Stock picking id", readonly=True)

    def action_confirm(self):
        """this is function calls the validate button of the sale.picking model"""
        self.stock_picking_id.button_validate(val=True)
