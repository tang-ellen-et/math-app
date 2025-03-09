import reflex as rx

# Id,Problem,Answer,Solution,Source,Year,Type,Competition,Difficulty,Img

class MathProblem(rx.Model, table=True):
    """The math problem model."""
    Problem: str
    Answer: str
    Solution: str
    Source: str
    Year: str
    Type: str
    Competition: str
    Difficulty: str
    Img: str

from enum import Enum

class DifficultLevel(Enum):
    High = "H", 
    Medium = "M",
    Low = "L"
class MathProblemSummary(rx.Model, table=True):
    """The math problem table view summary model."""
    Problem: str
    Source: str
    Year: str
    Type: str
    Competition: str
    Difficulty: str


class Customer(rx.Model, table=True):
    """The customer model."""
    problem: str
    email: str
    phone: str
    address: str


class Cereals(rx.Model, table=True):
    """The cereal model."""

    name: str
    mfr: str
    type: str
    calories: str
    protein: str
    fat: str
    sodium: str
    fiber: str
    carbo: str
    sugars: str
    potass: str
    vitamins: str
    shelf: str
    weight: str
    cups: str
    rating: str


class Covid(rx.Model, table=True):
    """The covid model."""

    state: str
    zone: str
    total_cases: str
    active: str
    discharged: str
    deaths: str
    active_ratio: str
    discharge_ratio: str
    discharge_avg: str
    death_ratio: str
    death_avg: str
    population: str


class Countries(rx.Model, table=True):
    """The countries model."""

    place: str
    pop1980: str
    pop2000: str
    pop2010: str
    pop2022: str
    pop2023: str
    pop2030: str
    pop2050: str
    country: str
    area: str
    landAreaKm: str
    cca2: str
    cca3: str
    netChange: str
    growthRate: str
    worldPercentage: str
    density: str
    densityMi: str
    rank: str
