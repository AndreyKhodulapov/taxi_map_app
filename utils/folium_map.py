import folium

from core.models import Point


def get_folium_map(
    center: Point,
    markers: list[Point],
    path: list[Point],
    distance: float,
    duration: float,
    zoom_level: int = 15
) -> folium.Map:
    map = folium.Map(
        location=[center.latitude, center.longitude],
        zoom_start=zoom_level
    )
    for idx, pt in enumerate(markers):
        label = "Начало поездки" if idx == 0 else "Конец поездки"
        color = "green" if idx == 0 else "red"
        folium.Marker(
            location=[pt.latitude, pt.longitude],
            popup=label,
            icon=folium.Icon(color=color)
        ).add_to(map)

    popup_html = (
        f"<b>Расстояние:</b> {distance:.1f} м<br>"
        f"<b>Время:</b> {duration:.1f} сек (~{duration / 60:.1f} мин)"
    )
    
    popup = folium.Popup(popup_html, max_width=300) 

    line = folium.PolyLine(
        locations=[(pt.latitude, pt.longitude) for pt in path],
        color="blue",
        weight=5,
        popup=popup
    )
    line.add_to(map)

    return map
