# -*- coding: utf-8 -*-

from odoo import fields, models


class DataSearchLines(models.TransientModel):
    _name = 'data.search.lines'
    _description = 'this is the order lines of the data search model'

    model_name = fields.Char(string="Model", help="model name of related search")
    field_name = fields.Char(string="Field", help="field name if there")
    value = fields.Char(string="Value", help="Value searched")
    data_search_id = fields.Many2one('data.search')
    record_id = fields.Integer()

    def view_model(self):
        """view button for the related records"""
        return {
            'type': 'ir.actions.act_window',
            'name': "View related data",
            'view_mode': 'form',
            'res_id': self.record_id,
            'res_model': f'{self.model_name}',
            'target': 'self',

        }
