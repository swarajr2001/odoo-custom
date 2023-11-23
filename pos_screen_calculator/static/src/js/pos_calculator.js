/** @odoo-module **/

import PosComponent from 'point_of_sale.PosComponent';
import ProductScreen from 'point_of_sale.ProductScreen';
import Registries from 'point_of_sale.Registries';
import { useListener } from "@web/core/utils/hooks";

export class PosCalculator extends PosComponent {
        setup() {
          super.setup();
          useListener('click', this.onClick);
      }
     async onClick() {
           const { confirmed} = await
                this.showPopup("CalculatorOperation", {
                  title: this.env._t('Calculator'),
                  body: this.env._t('Body of the popup'),
              });
     }
  }

PosCalculator.template = 'PosCalculator';

ProductScreen.addControlButton({
    component: PosCalculator

});

Registries.Component.add(PosCalculator);
