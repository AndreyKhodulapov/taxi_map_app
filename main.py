import requests

from core.models import Point, OSRMResponse


host = "http://router.project-osrm.org"
service = "route"
version = "v1"
profile = "driving"

# coordinates
kazan_cathedral = Point(longitude=30.323885, latitude=59.934214)
winter_palace = Point(longitude=30.313621, latitude=59.939763)

coordinates = f"{kazan_cathedral.longitude},{kazan_cathedral.latitude};{winter_palace.longitude},{winter_palace.latitude}"

url = f"{host}/{service}/{version}/{profile}/{coordinates}?overview=full&geometries=geojson"

response = requests.get(url)

data = OSRMResponse.model_validate(response.json())

print(data.routes[0].geometry.coordinates)

# print("Cтатус ответа:", response.status_code)
# print("Ответ от сервера:")
# print(response.text)
