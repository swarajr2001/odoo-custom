# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class RentRequest(models.Model):
    """"rent request fields and models"""
    _name = "vehicle.request"
    _inherit = 'mail.thread'
    _description = "contains the field for the rent request form"
    _rec_name = 'sequence'

    sequence = fields.Char(required=True,
                           readonly=True, default=lambda self: _('New'), copy=False)

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer",
        required=True, readonly=False, change_default=True, index=True,
        tracking=1)
    request_date = fields.Date(default=datetime.today(), string="Request date")
    vehicle_id = fields.Many2one("vehicle.details", tracking=1, string="Vehicle", required="True",
                                 domain="[('state', 'in',['available'])]")
    from_date = fields.Date(string="From date", default=datetime.today(), required=True)
    to_date = fields.Date(string="To date", required=True)
    period = fields.Integer(compute='_compute_period', store=True)
    states = fields.Selection(string="state", tracking=1, selection=[('draft', 'Draft'),
                                                                     ('confirm', 'Confirm'),
                                                                     ('invoiced', 'Invoiced'),
                                                                     ('returned', 'Returned')], default="draft")

    period_id = fields.Many2one("rent.charge", string="Period type",
                                domain="[('vehicle_details_id', '=', vehicle_id)]")

    rent = fields.Float(string="Rent", compute="_compute_rent", store=True)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    warning = fields.Boolean(string="Warning", default=False)
    late = fields.Boolean(string="late", default=False)
    invoice_id = fields.Many2one(
        comodel_name='account.move',
        string='Invoice',
    )
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    check_paid = fields.Boolean(default=False, compute='_check_invoice_paid')

    def _compute_warning(self):
        today = datetime.today()
        search_domain = ['|', ('to_date', '=', today),
                         '|', ('to_date', '=', today + timedelta(days=1)),
                         ('to_date', '=', today + timedelta(days=2))]

        find_val = self.search(search_domain)
        find_val.warning = True
        find_val.late = False
        find_val = self.search(
            [('states', '=', ['returned'])])
        find_val.warning = False
        find_val.late = False

    def _compute_late(self):
        find = self.search(
            [('to_date', '<', datetime.today()), ('states', '=', ['confirm'])])
        find.warning = False
        find.late = True
        find = self.search(
            [('states', '=', ['returned'])])
        find.warning = False
        find.late = False

    def _compute_schedule(self):
        self._compute_late()
        self._compute_warning()

    @api.depends('from_date', 'to_date')
    def _compute_period(self):
        """function to compute the period in request form"""

        for rec in self.filtered(lambda line: line.from_date and line.to_date):
            rec.period = (rec.to_date - rec.from_date).days
            if rec.to_date < datetime.today().date():
                rec.late = True
                rec.warning = False
            else:
                if rec.to_date == datetime.today().date():
                    rec.warning = True
                    rec.late = False
                elif rec.to_date == datetime.today().date() + timedelta(days=1):
                    rec.warning = True
                elif rec.to_date == datetime.today().date() + timedelta(days=2):
                    rec.warning = True
                elif rec.to_date < datetime.today().date():
                    rec.late = True
                    rec.warning = False
                else:
                    rec.warning = False

    @api.onchange('period_id', 'period')
    def _compute_rent(self):
        """function to compute rent based on the selected period"""
        for line in self:

            if line.period_id.time == 'day':
                line.rent = line.period * line.period_id.amount
            elif line.period_id.time == 'hour':
                line.rent = (line.period * 24) * line.period_id.amount
            elif line.period_id.time == 'week':
                line.rent = line.period * (line.period_id.amount / 7)
            elif line.period_id.time == 'month':
                line.rent = line.period * (line.period_id.amount / 30)
            else:
                line.rent = line.vehicle_id.rent

    def action_confirm(self):
        """button function applies on clicking confirm button"""
        self.states = "confirm"
        self.vehicle_id.state = 'not available'

    def action_return(self):
        """Button function applies on clicking return button"""
        for record in self:
            record.sudo().states = 'returned'
            record.sudo().late = False
            record.sudo().warning = False
            record.vehicle_id.sudo().state = 'available'
        return True

    @api.constrains('from_date', 'to_date')
    def _check_date_range(self):
        """function to check to date is earlier than from date"""
        for rec in self.filtered(lambda line: line.from_date and line.to_date and line.from_date > line.to_date):
            raise ValidationError("From date must be earlier than To date.")

    @api.model
    def create(self, vals):
        """function to create sequence in request form"""
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code(
                'vehicle.request') or _('New')
        res = super(RentRequest, self).create(vals)
        return res

    def action_order_processing(self):
        self.states = 'invoiced'
        for record in self:
            # Create a new delivery invoice
            product_id = self.env['product.product'].search([('name', '=', 'Rental Service')], limit=1)
            if not product_id:
                # Create the product 'Rental Service' if it doesn't exist
                product_id = self.env['product.product'].create({
                    'name': 'Rental Service',
                    'type': 'service',
                    'list_price': record.rent,
                    'standard_price': record.rent,
                })
            delivey_invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'invoice_date': record.request_date,
                'partner_id': record.partner_id.id,
                'currency_id': record.currency_id.id,
                'amount_total': record.rent,
                'invoice_line_ids': [(0, None, {
                    'product_id': product_id.id,
                    'name': record.vehicle_id.name,
                    'quantity': 1,
                    'price_unit': record.rent,
                    'price_subtotal': record.rent,
                })],
            })
            record.invoice_id = delivey_invoice.id
            delivey_invoice.action_post()
            return {
                'type': 'ir.actions.act_window',
                'name': 'Invoice',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': self.invoice_id.id,
                'target': 'current',
            }

    def view_invoice(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': self.invoice_id.id,
            'target': 'current',
        }

    def _check_invoice_paid(self):
        if self.invoice_id.payment_state == 'paid':
            self.check_paid = True
        else:
            self.check_paid = False
