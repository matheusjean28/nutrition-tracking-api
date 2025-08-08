from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import date as date_type, datetime
from pydantic import field_validator

class DailyGoal(SQLModel, table=True):
    """Daily nutrition goals for a user"""
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date_type = Field(default_factory=date_type.today, index=True)
    target_calories: float = Field(gt=0, description="Target calories for the day")
    target_water_ml: float = Field(gt=0, description="Target water intake in milliliters")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class FoodEntry(SQLModel, table=True):
    """Individual food consumption entries"""
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date_type = Field(default_factory=date_type.today, index=True)
    food_name: str = Field(min_length=1, description="Name of the food item")
    calories: float = Field(ge=0, description="Calories consumed")
    meal_type: str = Field(description="Type of meal: breakfast, lunch, dinner, snack")
    created_at: datetime = Field(default_factory=datetime.now)

    @field_validator('meal_type')
    @classmethod
    def validate_meal_type(cls, v):
        allowed_types = ['breakfast', 'lunch', 'dinner', 'snack']
        if v.lower() not in allowed_types:
            raise ValueError(f'meal_type must be one of: {", ".join(allowed_types)}')
        return v.lower()

class WaterEntry(SQLModel, table=True):
    """Individual water consumption entries"""
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date_type = Field(default_factory=date_type.today, index=True)
    amount_ml: float = Field(gt=0, description="Amount of water in milliliters")
    created_at: datetime = Field(default_factory=datetime.now)

class DailyProgressResponse(SQLModel):
    """Response model for daily progress"""
    date: date_type
    target_calories: float
    consumed_calories: float
    calories_percentage: float
    remaining_calories: float
    target_water_ml: float
    consumed_water_ml: float
    water_percentage: float
    remaining_water_ml: float
    food_entries: List[FoodEntry]
    water_entries: List[WaterEntry]

class NutritionSummary(SQLModel):
    """Summary of nutrition data"""
    total_days_tracked: int
    average_calories_percentage: float
    average_water_percentage: float
    days_met_calorie_goal: int
    days_met_water_goal: int
