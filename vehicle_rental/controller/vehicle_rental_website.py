# -*- coding: utf-8 -*-
from odoo.http import Controller, request, route
from odoo import http


class VehicleRequest(Controller):
    @route('/vehicle', auth='user', website=True)
    def vehicle_request(self):
        """this views all the requested created by the current user"""
        user_id = request.env.user.id
        print(user_id)
        request_details = request.env['vehicle.request'].search([('create_uid', '=', user_id)])
        return request.render('vehicle_rental.vehicle_request_tree_view',
                              {'request_details': request_details})

    @route('/create', auth='user', website=True)
    def create_request(self):
        """this function returns the template to create a vehicle rental request through website"""
        partner_ids = request.env['res.partner'].search([])
        vehicle_ids = request.env['vehicle.details'].search([])

        return request.render('vehicle_rental.vehicle_request_template',
                              {'partner_ids': partner_ids,
                               'vehicle_ids': vehicle_ids})

    @route('/create/rentRequest', auth='user', website=True)
    def create_rental_request(self, **kw):
        """this Creates button function create a rental request and returns to success window"""
        print(kw)
        if kw.get('period_type') != 'select a period':
            rent_request = request.env['vehicle.request'].sudo().create({
                'partner_id': kw.get('customer'),
                'request_date': kw.get('req_date'),
                'to_date': kw.get('toDate'),
                'from_date': kw.get('fromDate'),
                'vehicle_id': kw.get('vehicle'),
                'period_id': kw.get('period_type'),
                'rent': kw.get('totalRent'),
            })
        else:
            rent_request = request.env['vehicle.request'].sudo().create({
                'partner_id': kw.get('customer'),
                'request_date': kw.get('req_date'),
                'to_date': kw.get('toDate'),
                'from_date': kw.get('fromDate'),
                'vehicle_id': kw.get('vehicle'),
                'rent': kw.get('rent'),
            })

        request_id = rent_request.sequence
        return request.render('vehicle_rental.vehicle_request_success',
                              {'request_id': request_id})

    @http.route('/vehicleRequest', type='json', auth='user', website=True)
    def my_controller_method(self, **kwargs):
        """this functions returns the period and its amount to the javascript to pass to website frontend """
        vals = []
        vehicle_id = int(kwargs.get('vehicle_id'))
        period_type = request.env['rent.charge'].search([])
        for val in period_type:
            if val.vehicle_details_id.id == vehicle_id:
                vals.append({
                    'id': val.id,
                    'period': val.time,
                    'amount': val.amount,
                    'rent': val.vehicle_details_id.rent,
                })
        print(vals)
        return vals

    @http.route('/rentTypeId', type='json', auth='user', website=True)
    def rent_id(self, **kwargs):
        rent_id = int(kwargs.get('period_id'))
        value = request.env['rent.charge'].browse(rent_id)
        rent = value.amount
        return rent

    @route(['''/view/request/<model("vehicle.request"):details>'''], auth='user', website=True)
    def view_request(self, details):
        """this function view the details of the selected vehicle request"""
        print("view", details)
        return request.render('vehicle_rental.vehicle_request_view', {'details': details})

    @route('/add/customer', auth='user', website=True)
    def add_partner(self):
        """this function returns the form for creating a new customer"""
        country_ids = request.env['res.country'].search([])
        return request.render('vehicle_rental.add_customer',
                              {'country_ids': country_ids})

    @route('/create/partner', auth='user', website=True)
    def create_partner(self, **kw):
        """this button function creates the customer"""
        print("create partner", kw)
        partner_id = request.env['res.partner'].sudo().create({
            'name': kw.get('name'),
            'email': kw.get('email'),
            'phone': kw.get('phone'),
            'street': kw.get('street'),
            'country_id': kw.get('country'),
        })
        return request.redirect('/create')
