/** @odoo-module **/
import ProductScreen from 'point_of_sale.ProductScreen';
import Registries from 'point_of_sale.Registries';
const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
const {useState} = owl;

export class PosComboPopUp extends AbstractAwaitablePopup{

    setup(){
    this.state = useState({
            products: [],
            check_count: [],
        });
    }

     ComboClicked(ev,product){
        console.log("hii")
        let val = {}
        val['product_id'] = product.product_id
        val['category'] = product.pos_category
        val['product'] = product.product_name

        const isValExists = this.state.check_count.some(item =>
        item.category === val.category && item.product === val.product && item.product_id === val.product_id
        );

        if (isValExists) {
            this.state.check_count = this.state.check_count.filter(item =>
                item.category !== val.category || item.product !== val.product || item.product_id !== val.product_id
            );
        } else {
            this.state.check_count.push(val);
        }

        const productId = product.product_id;
        const isSelected = this.state.products.includes(productId);
        if (isSelected) {
            this.state.products = this.state.products.filter(id => id !== productId);
        } else {
            this.state.products.push(productId);
        }
        console.log("Selected Products: ", this.state.products);

        let count = 0;

        for (const val of this.state.check_count) {
          if (val.category == product.pos_category) {
            count++;
          }
        }

        if(count > product.max_count){
            const index = this.state.products.indexOf(product.product_id);
            this.state.products.splice(index, 1)
            const { confirmed } = this.showPopup('ComboLimit', {
                        title:'Combo alert',
                        body: 'You have already selected maximum item for this category!',
                        confirmText: 'Ok',
                    });
        }

        console.log("current-state",this.state.products)

    }

    Confirm(ev){
      console.log("confirm", this.state.products)
      var order = this.env.pos.get_order();
      for(let val in this.props.data){
          if(this.props.data[val].is_required == true){
              for(let product in this.props.data[val].products){
                this.state.products.push(this.props.data[val].products[product].product_id);
              }
          }
      }

      order.add_product(this.props.this_product)
      var products = this.state.products
      for(let product in products){
         order.add_product(this.env.pos.db.product_by_id[products[product]]);
      }
      this.confirm();
    }


    Close(ev){
         this.confirm();
    }

}
PosComboPopUp.template = 'PosComboPopUp';
Registries.Component.add(PosComboPopUp);


