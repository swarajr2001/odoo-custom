# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSetting(models.TransientModel):
    """this abstract class defines the field for api key of weather"""
    _inherit = "res.config.settings"
    weather_key = fields.Char(config_parameter='weather_key', string="weather api key")
    is_weather_option_enabled = fields.Boolean(config_parameter='weather_key_isTrue', string="option enabled")
    weather_location = fields.Char(config_parameter='weather_location', string="weather location")

    @api.model
    def custom_function(self):
        """this function is called from js to get res.config.settings values"""
        return {
            'weather_key': self.env['ir.config_parameter'].sudo().get_param('weather_key'),
            'weather_location': self.env['ir.config_parameter'].sudo().get_param('weather_location'),
            'weather_enabled': self.env['ir.config_parameter'].sudo().get_param('weather_key_isTrue'),
        }

    @api.onchange('is_weather_option_enabled')
    def change_field_value(self):
        if not self.is_weather_option_enabled:
            self.weather_key = False
            self.weather_location = False
