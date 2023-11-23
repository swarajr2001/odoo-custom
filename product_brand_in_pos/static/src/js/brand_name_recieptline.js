odoo.define('product_brand_in_pos.brand', function (require) {
'use strict';
        var { Orderline } = require('point_of_sale.models');
        var Registries = require('point_of_sale.Registries');

        const CustomOrderline = (Orderline) => class CustomOrderline extends Orderline{
               export_for_printing(){
                    var result = super.export_for_printing();
                    result.brand = this.get_product().brand;
                    return result;
               }
        }
        Registries.Model.extend(Orderline, CustomOrderline);
});