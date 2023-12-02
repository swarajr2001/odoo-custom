/** @odoo-module **/
import ProductScreen from 'point_of_sale.ProductScreen';
import Registries from 'point_of_sale.Registries';
const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
const {useState} = owl

export class PosComboPopUp extends AbstractAwaitablePopup{



}
PosComboPopUp.template = 'PosComboPopUp';
Registries.Component.add(PosComboPopUp);
