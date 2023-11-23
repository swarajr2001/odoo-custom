/** @odoo-module **/
import ProductScreen from 'point_of_sale.ProductScreen';
import Registries from 'point_of_sale.Registries';
const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
const {useState} = owl

export class CalculatorOperation extends AbstractAwaitablePopup{
    setup() {
      this.state = useState({
        current_input : '',
        value : '',
        answer : '',
      })
      super.setup();
    }

    sendInput(input){
        if (!isNaN(input) && typeof +input === 'number') {
            this.state.value += input
            this.state.current_input += input
        }

        else if(input == '.'){
             this.state.current_input += input
             this.state.value += input
             var check_vals = this.state.value.slice(-2)
             if (check_vals == '..'){
                this.state.value = ''
                this.state.current_input = 'Error'
             }
             else{
             }
        }

        else if(input == '+'){
            this.state.current_input = ''
            this.state.value = this.state.value + " " + input
        }

        else if(input == '-'){
            this.state.current_input = ''
            this.state.value = this.state.value + " " + input
        }

        else if(input == 'x'){
            this.state.current_input = ''
            this.state.value = this.state.value  + '*'
        }

        else if(input == '%'){
            this.state.current_input = ''
            this.state.value = this.state.value + " " + '%'
        }
        else if(input == '/'){
            this.state.current_input = ''
            this.state.value = this.state.value + " " + '/'
        }


        else if (input == 'Backspace'){
            try{
                this.state.current_input = this.state.current_input.slice(0, -1);
                this.state.value = this.state.value.slice(0, -1);
                }
            catch(err){
            this.state.current_input = ''
            }
        }
        else if (input == '='){
            try{
                if(this.state.answer != ''){
                     this.state.answer =  eval(this.state.value)
                     this.state.current_input =  this.state.answer
                     this.state.value = this.state.answer

                }
                else{
                    this.state.current_input = eval(this.state.value)
                    this.state.answer = this.state.current_input
                    }
                }
            catch(err){
                   this.state.current_input = 'Error'
            }
        }
        else{
            this.state.value = ''
            this.state.current_input = ''
        }
    }
}
CalculatorOperation.template = 'CalculatorNumber';
Registries.Component.add(CalculatorOperation);
