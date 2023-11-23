# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import fields, models, _, api


class MaterialRequest(models.Model):
    """model for the material request"""
    _name = "material.request"
    _rec_name = 'reference_no'
    _description = "this is a model for material request"
    _order = 'employee_id desc'

    employee_id = fields.Many2one("res.partner", string="Name", required=True, default=lambda self: self.env.user.partner_id)
    date = fields.Date(string="Request date", default=datetime.today())
    materials_ids = fields.One2many('oder.line', "material_req_id")
    reference_no = fields.Char(string='Order Reference', required=True,
                               readonly=True, default=lambda self: _('New'))
    is_purchased = fields.Boolean()
    is_internal_transfer = fields.Boolean(default=False)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approval-1', 'Manager approved'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='draft')
    purchase_ids = fields.Many2many("purchase.order")
    internal_ids = fields.Many2many("stock.picking")
    rfq_count = fields.Integer()
    internal_transfer_count = fields.Integer()

    @api.model
    def create(self, vals):
        print(vals)
        """function to create sequence number"""
        if vals.get('reference_no', _('New')) == _('New'):
            vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                'material.request') or _('New')
        res = super(MaterialRequest, self).create(vals)
        return res

    def submit(self):
        """button submit"""
        self.state = 'submitted'

    def approved(self):
        """Approved button function """
        self.state = 'approved'
        for record in self.materials_ids:
            if record.method == 'purchase':
                for line in record.material_id.variant_seller_ids:
                    self.rfq_count += 1
                    purchase_order = self.env['purchase.order'].create({
                        "partner_id": line.partner_id.id,
                        'origin': self.reference_no,
                    })
                    self.purchase_ids = [fields.Command.link(purchase_order.id)]
                    self.is_purchased = True
                    purchase_order.order_line = [fields.Command.create({
                        'product_id': record.material_id.id,
                        'name': record.material_id.name,
                        'product_uom_qty': 1,
                    })]
            if record.method == 'internal_transfer':
                self.internal_transfer_count += 1
                self.is_internal_transfer = True
                internal_transfer = self.env['stock.picking'].create({
                    "partner_id": self.employee_id.id,
                    'picking_type_id': self.env.ref('stock.picking_type_internal').id,
                    "origin": self.reference_no,
                    "location_id": record.source_location_id.id,
                    "location_dest_id": record.destination_location_id.id,
                })
                self.internal_ids = [fields.Command.link(internal_transfer.id)]
                internal_transfer.move_ids = [fields.Command.create({
                    'name': record.material_id.name,
                    'product_id': record.material_id.id,
                    'product_uom_qty': 1,
                    "location_id": record.source_location_id.id,
                    "location_dest_id": record.destination_location_id.id,
                })]
                self.internal_ids.action_confirm()

    def internal_transfer(self):
        """smart button internal transfer in the material request"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'internal transfer',
            'res_model': 'stock.picking',
            'view_mode': 'tree',
            'domain': [('id', 'in', self.internal_ids.ids)],
            'target': 'current',
        }

    def view_rfq(self):
        """function of smart button to view the created rfq"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase order',
            'res_model': 'purchase.order',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.purchase_ids.ids)],
            'target': 'current',
        }

    def approve(self):
        """function of button approve"""
        self.state = 'approval-1'

    def reject(self):
        """function of button reject """
        self.state = 'rejected'



