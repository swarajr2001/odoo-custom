# -*- coding: utf-8 -*-

from odoo import fields, models


class DataSearch(models.TransientModel):
    _name = 'data.search'
    _description = 'this model function get specified data from all odoo models'

    value_entered = fields.Char("Enter anything", required=True, help="value that is to search the entire odoo")
    model_ids = fields.Many2many('ir.model', string="Choose model", help="model in witch search is going")
    avoiding_model_ids = fields.Many2many('ir.model', 'avoiding', string="Choose avoiding model",
                                          help="model that is going to avoid from search if entire model is considered")
    field_id = fields.Many2one('ir.model.fields', help="field value that is going to search")
    search_line_ids = fields.One2many('data.search.lines', 'data_search_id',
                                      help="lines of data after search operation completed")

    def data_search(self):
        """button function to search data based on criteria"""
        self.search_line_ids = [fields.Command.clear()]
        if self.model_ids:
            models = self.model_ids
            for model in models:
                self.iterate_function(model.model)
        elif self.avoiding_model_ids:
            avoiding_models = ['data.search', 'data.search.lines']
            models = self.avoiding_model_ids
            for model in models:
                avoiding_models.append(model.model)
            all_models = self.env['ir.model'].search([('model', 'not in', avoiding_models)])
            for model in all_models:
                self.iterate_function(model.model)
        else:
            all_models = self.env['ir.model'].search([('model', 'not in', ['data.search', 'data.search.lines'])])
            for model in all_models:
                self.iterate_function(model.model)

    def iterate_function(self, model):
        """this function is called from the data_search function to create the tree view"""
        try:
            records = self.env[f'{model}'].sudo().search([])
            data_to_search = self.value_entered
            for each in records:
                each_dict = each.read()
                each_dict = each_dict[0]
                if self.field_id:
                    if data_to_search.lower() in str(each_dict[f'{self.field_id.name}']).lower():
                        search_lines = self.env['data.search.lines'].create({
                            'model_name': model,
                            'field_name': self.field_id.name,
                            'value': str(each_dict[f'{self.field_id.name}']),
                            'record_id': each_dict['id']
                        })
                        self.search_line_ids = [fields.Command.link(search_lines.id)]
                        self.env.cr.commit()
                else:
                    for key, value in each_dict.items():
                        if data_to_search.lower() in str(value).lower() and len(str(value).lower()) < 50:
                            search_lines = self.env['data.search.lines'].create({
                                'model_name': model,
                                'field_name': key,
                                'value': value,
                                'record_id': each_dict['id'],
                            })
                            self.search_line_ids = [fields.Command.link(search_lines.id)]
                            self.env.cr.commit()
        except:
            self.env.cr.rollback()

    def name_get(self):
        """name_get function to get the best clarification of the data"""
        result = []
        for rec in self:
            result.append((rec.id, '%s' % rec.value_entered))
        return result
