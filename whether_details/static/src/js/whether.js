/** @odoo-module **/
import { registry} from "@web/core/registry"
const { Component,useState} = owl
const rpc = require('web.rpc')

class Whether extends Component {
  async setup() {
    this.state = useState({
      is_option_enabled: false,
      values: {},
    });

    var settings_data = await rpc.query({
      model: "res.config.settings",
      method: "custom_function",
    });
    this.location = settings_data['weather_location']
    this.weather_key = settings_data['weather_key']
    this.state.is_option_enabled = settings_data["weather_enabled"];
  }

    onClick(ev){
        if(ev.location == false){
            if (navigator.geolocation)
            {
                navigator.geolocation.getCurrentPosition(successFunction);
            }
            else
            {
                alert('It seems like Geolocation, which is required for this page, is not enabled in your browser.');
            }

            function successFunction(position){
                var lat = position.coords.latitude;
                var long = position.coords.longitude;
                fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${long}&appid=${ev.weather_key}`)
                .then(response => response.json())
                .then(function(data) {
                 var datas = data
                 updateValue(datas)
                })
            }
        }
        else{
            fetch(`https://api.openweathermap.org/data/2.5/weather?appid=${ev.weather_key}&q=${ev.location}`)
            .then(response => response.json())
            .then(function(data) {
            var data_get = data
            updateValue(data_get)
            })
        }

        function updateValue(data){
            console.log("function called")
            if (data['cod'] != 401){
                if(data['message'] === "city not found"){
                    dict = {
                        'message':'unknown',
                    }
                     console.log(dict)
                     ev.state.values = dict
                }
                else{
                   var temp = data['main']['feels_like']
                   var temp_max = data['main']['temp_max']
                   var temp_min = data['main']['temp_min']
                   var temp_max = temp_max - 273.15
                   temp_max = Math.ceil(temp_max)
                   var temp_min = temp_min - 273.15
                   temp_min = Math.round(temp_min)
                   var celsius = temp - 273.15
                   celsius = Math.ceil(celsius)
                    var date = new Date();
                    var dict={
                    'humidity':data['main']['sea_level'],
                    'cloud':data['weather'][0]['description'],
                    'location': data['name'],
                    'max_temp':temp_max,
                    'min_temp':temp_min,
                    'day_temp':celsius,
                    'date': date,
                    'message':"location",
                    }
                    console.log(dict)
                     ev.state.values = dict
                }

            }
            else{
                var dict = {
                'message': 'error'
                }
                ev.state.values = dict
                }
        }
    }

}
Whether.template="Whether";
const Systray = {
       Component: Whether,
}
registry.category("systray").add("Whether", Systray)