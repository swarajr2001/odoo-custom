# -*- coding: utf-8 -*-
from odoo import api, fields, models


class VehicleDetails(models.Model):
    """vehicle fields in the form"""
    _name = "vehicle.details"
    _inherit = 'mail.thread'
    _description = "Vehicle Details"

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle", required="True",
                                 domain="[('state_id', 'in',['Registered'])]", tracking=True)
    request_count = fields.Integer(string="Request count", compute="compute_count")
    brand = fields.Char(string="Brand", related="vehicle_id.brand_id.name", store=True)
    year_field = fields.Char(string='Model year', compute='_compute_year',
                             store=True)
    name = fields.Char(string="Vehicle Name", compute='_compute_name', default="", store=True)
    rent = fields.Float(string="Rent", tracking=True, required=True, options="{'currency_field': 'currency_id'}")
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    state = fields.Selection(string="Status", selection=[('available', 'Available'),
                                                         ('not available', 'Not Available'),
                                                         ('sold', 'Sold')], default="available", tracking=True)
    req_ids = fields.One2many("vehicle.request", "vehicle_id",
                              domain=[('states', '=', 'confirm')])
    amount_ids = fields.One2many('rent.charge', 'vehicle_details_id')

    @api.depends('vehicle_id')
    def _compute_year(self):
        """function to compute the model year"""
        for record in self:
            record.year_field = str(
                record.vehicle_id.registration_date.year) if record.vehicle_id.registration_date else ""

    @api.depends('vehicle_id', 'year_field')
    def _compute_name(self):
        """function to compute the name in the vehicle rental form for required format"""
        for record in self:
            record.name = "{}/{}".format(record.vehicle_id.brand_id.name,
                                         record.vehicle_id.model_id.name) if record.year_field == "" else "{}/{}/{}".format(
                record.vehicle_id.brand_id.name, record.vehicle_id.model_id.name, record.year_field)

    def req_created(self):
        """button function of smart tab in the vehicle rental"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Requests',
            'view_mode': 'tree,form',
            'res_model': 'vehicle.request',
            'context': "{'create': False}"
        }

    @api.depends('vehicle_id')
    def compute_count(self):
        """function to display the number count in the smart tab"""
        for record in self:
            record.request_count = self.env['vehicle.request'].search_count(
                [('vehicle_id', '=', record.id)])

