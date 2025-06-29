from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from pyowm.utils.timestamps import next_three_hours
from pprint import pprint

owm = OWM("db38706ff6aeeadf1591ac7e1321954b")
mgr = owm.weather_manager()
observation = mgr.weather_at_place("Ivano-Frankivsk, UA")
w = observation.weather


weather_info = {
    "Status": w.detailed_status,
    "Wind": w.wind(),
    "Humidity": w.humidity,
    "Temperature": w.temperature("celsius"),
    "Rain": w.rain,
    "Clouds": w.clouds,
}
pprint(f"weather is {weather_info}")

forecast = mgr.forecast_at_place("Ternopil, UA", "3h")
answer = forecast.will_be_cloudy_at(timestamps.next_three_hours())
print(f"Answer is {answer}")
