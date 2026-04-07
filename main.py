import requests

from core.models import Point, OSRMResponse
from utils.folium_map import get_folium_map

# Интересно, но сыро, что пиздец
# TODO посмотреть че там за дз на бусти
# TODO подключить сервер и ручку с формой ввода
# TODO апи чтоб по названию находил координаты
# TODO автоцентровка карты
# TODO ручка отдавать карту с возвратом к исходной форме
# TODO деплой
# TODO личный кабинет
# TODO aрхив запросов через postgres

host = "http://router.project-osrm.org"
service = "route"
version = "v1"
profile = "driving"

# coordinates
start_point = Point(longitude=30.304768, latitude=59.980180)
end_point = Point(longitude=30.296093, latitude=59.925619)
center_point = Point(longitude=30.318301, latitude=59.938333)

coordinates = f"{start_point.longitude},{start_point.latitude};{end_point.longitude},{end_point.latitude}"

url = f"{host}/{service}/{version}/{profile}/{coordinates}?overview=full&geometries=geojson"

response = requests.get(url)

data = OSRMResponse.model_validate(response.json())

route = data.routes[0]

folium_map = get_folium_map(
    center=center_point,
    markers=[start_point, end_point],
    zoom_level=15,
    path=route.geometry.coordinates,
    distance=route.distance,
    duration=route.duration
)

output_file = "route_map.html"
folium_map.save(output_file)

# print(data.routes[0].geometry.coordinates)
