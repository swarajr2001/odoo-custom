# -*- coding: utf-8 -*-

from odoo import fields, models, _
import xmlrpc.client

from odoo.exceptions import UserError


class ProductTemplate(models.TransientModel):
    """wizard for giving the database credential and getting product data from odoo 15"""
    _name = 'product.migrate'
    _description = 'inherited product.template to add functionality to get data from odoo15'

    new_database = fields.Char(string="New database", default="odoo16", required=True)
    new_database_url = fields.Char(string="new database Url", default="http://localhost:8016", required=True)
    new_database_username = fields.Char(string="New database username", required=True)
    new_database_password = fields.Char(string="New database password", required=True)

    old_database = fields.Char(string="Old database", default="odoo15", required=True)
    old_database_url = fields.Char(string="Old database Url", default="http://localhost:", required=True)
    old_database_username = fields.Char(string="Old database username", required=True)
    old_database_password = fields.Char(string="Old database password", required=True)

    def action_confirm(self):
        """function to retrieve data from odoo 15 to odoo 16"""
        try:
            common_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.new_database_url))
            models_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.new_database_url))
            version_db1 = common_1.version()

            common_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.old_database_url))
            models_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.old_database_url))
            version_db2 = common_2.version()

            uid_db1 = common_1.authenticate(self.new_database, self.new_database_username, self.new_database_password,
                                            {})
            uid_db2 = common_2.authenticate(self.old_database, self.old_database_username, self.old_database_password,
                                            {})

            product_data = models_2.execute_kw(self.old_database, uid_db2, self.old_database_password,
                                               'product.template', 'search_read', [],
                                               {'fields': ['name', 'detailed_type', 'list_price', 'standard_price',
                                                           'default_code', 'invoice_policy', 'image_1920']})
            all_product_odoo16 = self.env['product.template'].search([])
            existing_product_data = all_product_odoo16.read(['name', 'detailed_type', 'list_price', 'standard_price',
                                                             'default_code', 'invoice_policy'])
            odoo16_data = []

            for item in existing_product_data:
                modified_dict = {key: value for key, value in item.items() if key != 'id'}
                odoo16_data.append(modified_dict)

            odoo15_data = []

            for item in product_data:
                modified_dict = {key: value for key, value in item.items() if key != 'id' and key != 'image_1920'}
                odoo15_data.append(modified_dict)
            new = []
            for data in odoo15_data:
                if data not in odoo16_data:
                    new.append(data)
            matching_dicts = []
            for items in new:
                matching_dict = next(
                    (values for values in product_data if all(values[key] == items[key] for key in items if key != 'image' and key != 'id')),
                    None)
                if matching_dict:
                    matching_dicts.append(matching_dict)

            print(matching_dicts)
            product_data_odoo16 = models_1.execute_kw(self.new_database, uid_db1, self.new_database_password,
                                                      'product.template', 'create', [matching_dicts])


        except:
            raise UserError(_("provide credentials is wrong"))
