# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class VehicleSnippet(http.Controller):
    @http.route('/view-vehicle-request', type="json", auth="public")
    def view_vehicle_request(self):
        """this functions returns the vehicle details in descending order of their request count"""
        vehicle_ids = request.env['vehicle.details'].search_read([])
        top_vehicle = sorted(vehicle_ids, key=lambda d: d['request_count'], reverse=True)
        print(top_vehicle)
        return top_vehicle

    @http.route('/view-details/<id>', auth='user', website=True)
    def view_request(self, id):
        """this function returns the corresponding clicked vehicle details in a new form"""
        vehicle_id = int(id)
        vehicle_details = request.env['vehicle.details'].browse(vehicle_id)
        vehicle_data = [{
            'name': vehicle_details.name,
            'brand': vehicle_details.brand,
            'rent': vehicle_details.rent,
            'model': vehicle_details.year_field
        }]
        print(vehicle_data)
        return request.render('vehicle_rental.vehicle_details_view', {'vehicle_data': vehicle_data})

    @http.route('/back-to-main', auth='user', website=True)
    def exit_to_main(self):
        return request.redirect('/')
