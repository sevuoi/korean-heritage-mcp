from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class HeritageIdentifier(BaseModel):
    designation_code: str | None = None
    designation_type: str = ""
    designation_number: int | None = None
    management_number: str | None = None
    city_code: str | None = None
    heritage_id: str = ""


class HeritageItem(BaseModel):
    heritage_id: str = ""
    name: str = ""
    designation_type: str | None = None
    designation_number: int | None = None
    former_name: str | None = None
    period: str | None = None
    designated_date: str | None = None
    address: str | None = None
    city: str | None = None
    district: str | None = None
    owner: str | None = None
    manager: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    summary: str | None = None
    description: str | None = None
    image_url: str | None = None
    source_url: str | None = None
    source_name: str = "국가유산청"
    raw_identifiers: HeritageIdentifier | None = None


class NearbyHeritageItem(BaseModel):
    heritage: HeritageItem
    distance_km: float
    map_url: str


class LocationPoint(BaseModel):
    name: str
    address: str | None = None
    road_address: str | None = None
    latitude: float
    longitude: float
    source: str


class NearbyFacility(BaseModel):
    name: str
    category: str
    address: str | None = None
    road_address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    distance_m: int | None = None
    phone: str | None = None
    place_url: str | None = None


class TripStop(BaseModel):
    order: int
    visit_place: str
    featured_heritage: list[str] = Field(default_factory=list)
    heritage: HeritageItem
    recommended_duration_minutes: int
    travel_minutes_from_previous: int | None = None
    travel_time_is_estimate: bool = True
    visit_note: str
    map_url: str


class TripDay(BaseModel):
    day: int
    title: str
    stops: list[TripStop] = Field(default_factory=list)
    meal_area: str | None = None
    parking_notes: list[str] = Field(default_factory=list)
    travel_notes: list[str] = Field(default_factory=list)


class HeritageTripPlan(BaseModel):
    region: str
    days: int
    transport: str
    theme_summary: str
    region_overview: str
    recommended_heritage: list[HeritageItem] = Field(default_factory=list)
    itinerary: list[TripDay] = Field(default_factory=list)
    food_suggestions: list[NearbyFacility] = Field(default_factory=list)
    verification_notes: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.now)


class ToolErrorModel(BaseModel):
    code: str
    message: str
    recoverable: bool
    required_input: list[str]
