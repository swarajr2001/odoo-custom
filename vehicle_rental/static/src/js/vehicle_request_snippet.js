odoo.define('vehicle_rental.dynamic_snippet', function (require) {
   var PublicWidget = require('web.public.widget');
    var core = require('web.core');
    var QWeb = core.qweb;

   var Dynamic = PublicWidget.Widget.extend({
       selector: '.dynamic_snippet_blog',


       start: function () {
           var self = this;
            var ajax = require('web.ajax');
            ajax.jsonRpc('/view-vehicle-request', 'call',{
                    })
                    .then(function (data) {
                    this.data = data;
                    var chunks = _.chunk(this.data, 4)
                    chunks[0].is_active = true
                    var rendered_html = QWeb.render('top_requested_vehicle',{chunks, 'c_id': Date.now()});
                    self.$el.find("#datacorosel").html(rendered_html)

           });
       },


   });

   PublicWidget.registry.dynamic_snippet_blog = Dynamic;
   return Dynamic;
});