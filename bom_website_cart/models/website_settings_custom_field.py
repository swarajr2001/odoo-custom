from odoo import api, fields, models
from odoo.tools._monkeypatches import literal_eval


class ConfSetting(models.TransientModel):
    """this abstract class defines the field for website inherited field"""
    _inherit = "res.config.settings"
    choose_product_ids = fields.Many2many('product.template', stote=True)

    def set_values(self):
        """this function helps to save values in the settings inherited choose_product_ids field"""
        res = super(ConfSetting, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('bom_website_cart.choose_product_ids',
                                                         self.choose_product_ids.ids)
        return res

    @api.model
    def get_values(self):
        """this function retrieve the value in the inherited choose_product_ids field"""
        res = super(ConfSetting, self).get_values()
        product_ids = self.env['ir.config_parameter'].sudo().get_param('bom_website_cart.choose_product_ids')
        res.update(
            choose_product_ids=[(6, 0, literal_eval(product_ids))
                                ] if product_ids else False, )
        return res

   