from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from datetime import date, datetime
from typing import List, Optional
import os

from models import (
    DailyGoal, FoodEntry, WaterEntry, 
    DailyProgressResponse, NutritionSummary
)
from database import create_db_and_tables, get_session

app = FastAPI(
    title="Nutrition Tracking API",
    description="A comprehensive nutrition tracking system for monitoring daily food and water intake",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    """Initialize database on application startup"""
    create_db_and_tables()

# Serve static files
@app.get("/", response_class=FileResponse)
def read_index():
    """Serve the main HTML page"""
    return FileResponse("index.html")

# Daily Goals Endpoints
@app.post("/goals/", response_model=DailyGoal)
def create_daily_goal(goal: DailyGoal, session: Session = Depends(get_session)):
    """Create or update daily nutrition goals"""
    # Check if goal already exists for this date
    existing_goal = session.exec(
        select(DailyGoal).where(DailyGoal.date == goal.date)
    ).first()
    
    if existing_goal:
        # Update existing goal
        existing_goal.target_calories = goal.target_calories
        existing_goal.target_water_ml = goal.target_water_ml
        existing_goal.updated_at = datetime.now()
        session.add(existing_goal)
        session.commit()
        session.refresh(existing_goal)
        return existing_goal
    else:
        # Create new goal
        session.add(goal)
        session.commit()
        session.refresh(goal)
        return goal

@app.get("/goals/{goal_date}", response_model=DailyGoal)
def get_daily_goal(goal_date: date, session: Session = Depends(get_session)):
    """Get daily goal for a specific date"""
    goal = session.exec(
        select(DailyGoal).where(DailyGoal.date == goal_date)
    ).first()
    
    if not goal:
        raise HTTPException(status_code=404, detail="Daily goal not found for this date")
    return goal

@app.get("/goals/", response_model=list[DailyGoal])
def list_daily_goals(session: Session = Depends(get_session)):
    """List all daily goals"""
    return session.exec(select(DailyGoal)).all()

# Food Entry Endpoints
@app.post("/food/", response_model=FoodEntry)
def add_food_entry(food: FoodEntry, session: Session = Depends(get_session)):
    """Add a food consumption entry"""
    session.add(food)
    session.commit()
    session.refresh(food)
    return food

@app.get("/food/{entry_id}", response_model=FoodEntry)
def get_food_entry(entry_id: int, session: Session = Depends(get_session)):
    """Get a specific food entry"""
    food = session.get(FoodEntry, entry_id)
    if not food:
        raise HTTPException(status_code=404, detail="Food entry not found")
    return food

@app.get("/food/", response_model=list[FoodEntry])
def list_food_entries(
    entry_date: Optional[date] = None, 
    session: Session = Depends(get_session)
):
    """List food entries, optionally filtered by date"""
    query = select(FoodEntry)
    
    if entry_date:
        query = query.where(FoodEntry.date == entry_date)
    
    return session.exec(query.order_by(FoodEntry.created_at)).all()

@app.put("/food/{entry_id}", response_model=FoodEntry)
def update_food_entry(
    entry_id: int, 
    food_update: FoodEntry, 
    session: Session = Depends(get_session)
):
    """Update a food entry"""
    food = session.get(FoodEntry, entry_id)
    if not food:
        raise HTTPException(status_code=404, detail="Food entry not found")
    
    food.food_name = food_update.food_name
    food.calories = food_update.calories
    food.meal_type = food_update.meal_type
    
    session.add(food)
    session.commit()
    session.refresh(food)
    return food

@app.delete("/food/{entry_id}")
def delete_food_entry(entry_id: int, session: Session = Depends(get_session)):
    """Delete a food entry"""
    food = session.get(FoodEntry, entry_id)
    if not food:
        raise HTTPException(status_code=404, detail="Food entry not found")
    
    session.delete(food)
    session.commit()
    return {"message": "Food entry deleted successfully"}

# Water Entry Endpoints
@app.post("/water/", response_model=WaterEntry)
def add_water_entry(water: WaterEntry, session: Session = Depends(get_session)):
    """Add a water consumption entry"""
    session.add(water)
    session.commit()
    session.refresh(water)
    return water

@app.get("/water/{entry_id}", response_model=WaterEntry)
def get_water_entry(entry_id: int, session: Session = Depends(get_session)):
    """Get a specific water entry"""
    water = session.get(WaterEntry, entry_id)
    if not water:
        raise HTTPException(status_code=404, detail="Water entry not found")
    return water

@app.get("/water/", response_model=list[WaterEntry])
def list_water_entries(
    entry_date: Optional[date] = None, 
    session: Session = Depends(get_session)
):
    """List water entries, optionally filtered by date"""
    query = select(WaterEntry)
    
    if entry_date:
        query = query.where(WaterEntry.date == entry_date)
    
    return session.exec(query.order_by(WaterEntry.created_at)).all()

@app.put("/water/{entry_id}", response_model=WaterEntry)
def update_water_entry(
    entry_id: int, 
    water_update: WaterEntry, 
    session: Session = Depends(get_session)
):
    """Update a water entry"""
    water = session.get(WaterEntry, entry_id)
    if not water:
        raise HTTPException(status_code=404, detail="Water entry not found")
    
    water.amount_ml = water_update.amount_ml
    
    session.add(water)
    session.commit()
    session.refresh(water)
    return water

@app.delete("/water/{entry_id}")
def delete_water_entry(entry_id: int, session: Session = Depends(get_session)):
    """Delete a water entry"""
    water = session.get(WaterEntry, entry_id)
    if not water:
        raise HTTPException(status_code=404, detail="Water entry not found")
    
    session.delete(water)
    session.commit()
    return {"message": "Water entry deleted successfully"}

# Progress and Analytics Endpoints
@app.get("/progress/{progress_date}", response_model=DailyProgressResponse)
def get_daily_progress(progress_date: date, session: Session = Depends(get_session)):
    """Get daily progress including percentage completion and remaining amounts"""
    # Get daily goal
    goal = session.exec(
        select(DailyGoal).where(DailyGoal.date == progress_date)
    ).first()
    
    if not goal:
        raise HTTPException(
            status_code=404, 
            detail="No daily goal found for this date. Please set a daily goal first."
        )
    
    # Get food entries for the date
    food_entries = session.exec(
        select(FoodEntry).where(FoodEntry.date == progress_date)
    ).all()
    
    # Get water entries for the date
    water_entries = session.exec(
        select(WaterEntry).where(WaterEntry.date == progress_date)
    ).all()
    
    # Calculate totals
    consumed_calories = sum(entry.calories for entry in food_entries)
    consumed_water_ml = sum(entry.amount_ml for entry in water_entries)
    
    # Calculate percentages
    calories_percentage = min(100.0, (consumed_calories / goal.target_calories) * 100)
    water_percentage = min(100.0, (consumed_water_ml / goal.target_water_ml) * 100)
    
    # Calculate remaining amounts
    remaining_calories = max(0, goal.target_calories - consumed_calories)
    remaining_water_ml = max(0, goal.target_water_ml - consumed_water_ml)
    
    return DailyProgressResponse(
        date=progress_date,
        target_calories=goal.target_calories,
        consumed_calories=consumed_calories,
        calories_percentage=round(calories_percentage, 2),
        remaining_calories=round(remaining_calories, 2),
        target_water_ml=goal.target_water_ml,
        consumed_water_ml=consumed_water_ml,
        water_percentage=round(water_percentage, 2),
        remaining_water_ml=round(remaining_water_ml, 2),
        food_entries=list(food_entries),
        water_entries=list(water_entries)
    )

@app.get("/progress/", response_model=DailyProgressResponse)
def get_today_progress(session: Session = Depends(get_session)):
    """Get today's progress"""
    return get_daily_progress(date.today(), session)

@app.get("/summary/", response_model=NutritionSummary)
def get_nutrition_summary(session: Session = Depends(get_session)):
    """Get overall nutrition tracking summary"""
    # Get all goals
    goals = session.exec(select(DailyGoal)).all()
    
    if not goals:
        return NutritionSummary(
            total_days_tracked=0,
            average_calories_percentage=0.0,
            average_water_percentage=0.0,
            days_met_calorie_goal=0,
            days_met_water_goal=0
        )
    
    total_days = len(goals)
    calories_percentages = []
    water_percentages = []
    days_met_calorie_goal = 0
    days_met_water_goal = 0
    
    for goal in goals:
        # Get entries for this date
        food_entries = session.exec(
            select(FoodEntry).where(FoodEntry.date == goal.date)
        ).all()
        water_entries = session.exec(
            select(WaterEntry).where(WaterEntry.date == goal.date)
        ).all()
        
        # Calculate totals
        consumed_calories = sum(entry.calories for entry in food_entries)
        consumed_water_ml = sum(entry.amount_ml for entry in water_entries)
        
        # Calculate percentages
        calorie_percentage = (consumed_calories / goal.target_calories) * 100
        water_percentage = (consumed_water_ml / goal.target_water_ml) * 100
        
        calories_percentages.append(calorie_percentage)
        water_percentages.append(water_percentage)
        
        # Check if goals were met
        if consumed_calories >= goal.target_calories:
            days_met_calorie_goal += 1
        if consumed_water_ml >= goal.target_water_ml:
            days_met_water_goal += 1
    
    # Calculate averages
    avg_calories_percentage = sum(calories_percentages) / len(calories_percentages)
    avg_water_percentage = sum(water_percentages) / len(water_percentages)
    
    return NutritionSummary(
        total_days_tracked=total_days,
        average_calories_percentage=round(avg_calories_percentage, 2),
        average_water_percentage=round(avg_water_percentage, 2),
        days_met_calorie_goal=days_met_calorie_goal,
        days_met_water_goal=days_met_water_goal
    )
if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
