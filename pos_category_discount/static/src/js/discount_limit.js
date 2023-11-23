/** @odoo-module **/
import ProductScreen from 'point_of_sale.ProductScreen';
import Registries from 'point_of_sale.Registries';

const ProductDiscount = (ProductScreen) => class ProductDiscount extends ProductScreen{
      async _onClickPay() {
           const product_list = []
           var max_discount_amount = this.env.pos.config.discount_limit
           var order_line = this.env.pos.get_order().orderlines
           var selected_product_category_ids = this.env.pos.config.product_category_ids
            console.log(this.env.pos.config)
           const list = []

           for(let key in selected_product_category_ids){
                    for(let val in order_line){
                        if(order_line[val].product.pos_categ_id[0]==selected_product_category_ids[key]){

                            list.push({
                                'product':order_line[val].product.display_name,
                                'discount':order_line[val].discount,
                                'price':order_line[val].price,
                                'quantity':order_line[val].quantity,
                            })
                        }
                    }
           }
           var total = 0
           for(let key in list){
                if(list[key].discount !=0){
                        var discounted_amount = (list[key].discount * list[key].price * list[key].quantity)/100
                        total+=discounted_amount
                }
           }
           if(total>max_discount_amount){
              this.showPopup('ConfirmPopup', {
                        title: this.env._t('Discount alert'),
                        body: this.env._t(
                            'You have exceeded the discount limit for current order'
                        ),
                    });
           }
           else{
                var result = super._onClickPay()
                return result
           }
}
}
Registries.Component.extend(ProductScreen, ProductDiscount);
