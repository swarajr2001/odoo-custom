odoo.define('vehicle_rental.example', function (require) {
"use strict";
var vehicle_rent=0
var publicWidget = require('web.public.widget')
publicWidget.registry.vehicleRequest = publicWidget.Widget.extend({
selector: '.container',
events: {
        'change #fromDate' : '_onChangeFromDate',
        'change #toDate' : '_onChangeToDate',
        'change #vehicle_ids': '_onVehicleChange',
        'change #period': '_getSelectedValue'
        },
            _getSelectedValue: function() {

            var selectedValue = $('#period').val();

            $("#periodId").val(selectedValue)
            var ajax = require('web.ajax');

            ajax.jsonRpc('/rentTypeId', 'call',{
                    'period_id' : selectedValue,
                    })
                    .then(function (data) {
                        $("#total").val(data)
                        vehicle_rent = data
                        var text = $("#period option:selected").text();
            if (text.trim() == 'day'){
                var period = $("#pType").val()
                var amount = vehicle_rent
                var total = period * amount
                console.log("day",total)
                $("#rent").val(total)

            }
            else if (text.trim() == 'hour'){
                    var period = $("#pType").val()
                    var amount = vehicle_rent
                    var total = period * amount * 24
                    total = Math.ceil(total)
                    $("#rent").val(total)
                }
                    else if(text.trim() == 'month'){
                    var period = $("#pType").val()
                    var period = period/30
                    var amount = vehicle_rent
                    var total = period * amount
                    total = Math.ceil(total)
                    $("#rent").val(total)
                }
                else if(text.trim() == 'week'){
                    var period = $("#pType").val()
                    var period = period/7
                    var amount = vehicle_rent
                    var total = period * amount
                    total = Math.ceil(total)
                    $("#rent").val(total)
                }
                else{
                    var non_type_rent = $("#demoRent").val()
                    $("#rent").val(non_type_rent)

                }


            })
          },

        start:function(){
            var fromDate = $("#fromDate").val()
            $('#toDate').attr('min', fromDate)

        },

        _onChangeFromDate: function(){
            var fromDate = $("#fromDate").val()
            $('#toDate').attr('min', fromDate)
            var toDate = $("#toDate").val()
            var start = new Date(fromDate);
            var end = new Date(toDate);
            var diffDate = (end - start) / (1000 * 60 * 60 * 24);
            var days = Math.round(diffDate);
            $("#pType").val(days)
            var text = $("#period option:selected").text();

                    if (text.trim() == 'day'){
                    var period = $("#pType").val()
                    var amount = vehicle_rent
                    var total = period * amount
                    total = Math.ceil(total)
                    console.log("day",total)
                    $("#rent").val(total)
                    }
                    else if (text.trim() == 'hour'){
                    var period = $("#pType").val()
                    var amount = vehicle_rent
                    var total = period * amount * 24
                    total = Math.ceil(total)
                    $("#rent").val(total)
                    }
                    else if(text.trim() == 'month'){
                    var period = $("#pType").val()
                    var period = period/30
                    var amount = vehicle_rent
                    var total = period * amount
                    total = Math.ceil(total)
                    $("#rent").val(total)
                }
                else if(text.trim() == 'week'){
                    var period = $("#pType").val()
                    var period = period/7
                    var amount = vehicle_rent
                    var total = period * amount
                    total = Math.ceil(total)
                    $("#rent").val(total)
                }
                else{
                    var non_type_rent = $("#demoRent").val()
                    $("#rent").val(non_type_rent)

                }

        },

        _onChangeToDate: function(){

            console.log($("#demoRent").val())
                var fromDate = $("#fromDate").val()
                var toDate = $("#toDate").val()
                var start = new Date(fromDate);
                var end = new Date(toDate);
                var diffDate = (end - start) / (1000 * 60 * 60 * 24);
                var days = Math.round(diffDate);
                $("#pType").val(days)
                var text = $("#period option:selected").text();

                    if (text.trim() == 'day'){
                    var period = $("#pType").val()
                    var amount = vehicle_rent
                    var total = period * amount
                    total = Math.ceil(total)
                    console.log("day",total)
                    $("#rent").val(total)
                    }
                    else if (text.trim() == 'hour'){
                    var period = $("#pType").val()
                    var amount = vehicle_rent
                    var total = period * amount * 24
                    total = Math.ceil(total)
                    $("#rent").val(total)
                    }
                    else if(text.trim() == 'month'){
                    var period = $("#pType").val()
                    var period = period/30
                    var amount = vehicle_rent
                    var total = period * amount
                    total = Math.ceil(total)
                    $("#rent").val(total)
                }
                else if(text.trim() == 'week'){
                    var period = $("#pType").val()
                    var period = period/7
                    var amount = vehicle_rent
                    var total = period * amount
                    total = Math.ceil(total)
                    $("#rent").val(total)
                }
                else{
                    var non_type_rent = $("#demoRent").val()
                    $("#rent").val(non_type_rent)

                }

        },
        _onVehicleChange: function(){
            $("#toDate").val(null)
            $("#pType").val(null)
            $("#rent").val(null)
            $(".option").remove();
            var ajax = require('web.ajax');
            var vehicle_id = $("#vehicle_ids").val()

            ajax.jsonRpc('/vehicleRequest', 'call',{
                    'vehicle_id' : vehicle_id,
                    })
            .then(function (data) {
                if(data.length != 0){
                    var rent = data[0].rent
                    $("#demoRent").val(rent)
                    }
                else{
                    var rent = 0
                    $("#demoRent").val(rent)
                }
                    $(".option").remove();
                    $.each(data, function(index, value) {
                        var val = value;
                        $('#period').append(`<option value="${val.id}" class="option">
                                                   ${val.period}
                                             </option>`);

                        });
                        });
        },



})
});