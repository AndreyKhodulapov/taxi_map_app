from typing import Any 

from pydantic import BaseModel, Field, computed_field


class Point(BaseModel):
    """Модель точки на карте"""
    longitude: float = Field(..., description="Долгота точки")
    latitude: float = Field(..., description="Широта точки")

    def __repr__(self) -> str:
        return f"({self.longitude}, {self.latitude})"


class Geometry(BaseModel):
    """Геометрия маршрута"""
    type: str = Field(..., description="Тип геометрии")
    raw_coordinates: list[list[float]] = Field(
        ..., 
        alias="coordinates",
        description="Список координат маршрута [широта, долгота]",
        exclude=True
    )

    @computed_field
    @property
    def coordinates(self) -> list[Point]:
        return [
            Point(longitude=coord[0], latitude=coord[1])
            for coord in self.raw_coordinates
        ]



class Leg(BaseModel):
    """Этап маршрута между двумя точками"""
    steps: list[Any] = Field(..., description="Список шагов маршрута")
    weight: float = Field(..., description="Вес маршрута")
    summary: str = Field(..., description="Описание маршрута")
    duration: float = Field(..., description="Длительность маршрута")
    distance: float = Field(..., description="Расстояние маршрута")


class Route(BaseModel):
    """Основной маршрут"""
    legs: list[Leg] = Field(..., description="Список легов маршрута")
    weight_name: str = Field(..., description="Название веса маршрута")
    geometry: Geometry = Field(..., description="Геометрия маршрута")
    weight: float = Field(..., description="Вес маршрута")
    duration: float = Field(..., description="Длительность маршрута")
    distance: float = Field(..., description="Расстояние маршрута")


class Waypoint(BaseModel):
    """Ключевая точка маршрута"""
    hint: str = Field(..., description="Подсказка")
    location: tuple[float, float] = Field(..., description="Координаты точки")
    name: str = Field(..., description="Название точки")
    distance: float = Field(..., description="Расстояние до точки")


class OSRMResponse(BaseModel):
    """Коневая модель ответа от OSRM"""
    code: str = Field(..., description="Код ответа")
    routes: list[Route] = Field(..., description="Список маршрутов")
    waypoints: list[Waypoint] = Field(..., description="Список ключевых точек")
