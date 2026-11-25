# Nutrition Tracking API

A comprehensive FastAPI-based nutrition tracking system that helps you monitor daily food and water intake with percentage-based progress tracking. The API provides endpoints to set daily goals, log consumption, and get real-time progress with remaining amounts.

## Features

- **Daily Goal Management**: Set and update target calories and water intake
- **Food Tracking**: Log food consumption with meal type categorization
- **Water Intake Monitoring**: Track water consumption throughout the day
- **Progress Analytics**: Get percentage completion and remaining amounts
- **Current State Endpoint**: Real-time view of today's progress
- **Historical Data**: Summary statistics across all tracked days

## Quick Start

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Installation

1. Clone or download the project files:
   ```bash
   git clone <your-repo-url>
   cd nutrition-tracker
   ```

2. Install dependencies:
   ```bash
   pip install fastapi uvicorn sqlmodel pydantic
   ```

3. Run the server:
   ```bash
   python main.py
   ```

4. Access the application:
   - **Web Interface**: http://localhost:5000
   - **API Documentation**: http://localhost:5000/docs
   - **Interactive API**: http://localhost:5000/redoc

## Project Structure

```
nutrition-tracker/
├── main.py          # FastAPI application with all endpoints
├── models.py        # Database models and response schemas
├── database.py      # Database configuration and session management
├── index.html       # Web interface (optional)
└── README.md        # This documentation
```

## Database

The application uses SQLite by default, automatically creating a `nutrition_data.db` file. For production, you can set the `DATABASE_URL` environment variable to use PostgreSQL or other databases.

### Database Schema

- **dailygoal**: Daily nutrition targets
- **foodentry**: Individual food consumption records
- **waterentry**: Water intake records

## API Documentation

### Base URL
```
http://localhost:5000
```

### Authentication
No authentication required (basic version).

---

## Daily Goals Endpoints

### Create or Update Daily Goal
**POST** `/goals/`

Set daily nutrition targets. If a goal already exists for the date, it will be updated.

**Request Body:**
```json
{
  "target_calories": 2000,
  "target_water_ml": 2500,
  "date": "2025-08-08"  // Optional, defaults to today
}
```

**Response:**
```json
{
  "id": 1,
  "date": "2025-08-08",
  "target_calories": 2000,
  "target_water_ml": 2500,
  "created_at": "2025-08-08T10:00:00",
  "updated_at": "2025-08-08T10:00:00"
}
```

### Get Daily Goal
**GET** `/goals/{date}`

Retrieve the daily goal for a specific date.

**Parameters:**
- `date` (path): Date in YYYY-MM-DD format

**Response:**
```json
{
  "id": 1,
  "date": "2025-08-08",
  "target_calories": 2000,
  "target_water_ml": 2500,
  "created_at": "2025-08-08T10:00:00",
  "updated_at": "2025-08-08T10:00:00"
}
```

### List All Goals
**GET** `/goals/`

Get all daily goals.

**Response:**
```json
[
  {
    "id": 1,
    "date": "2025-08-08",
    "target_calories": 2000,
    "target_water_ml": 2500,
    "created_at": "2025-08-08T10:00:00",
    "updated_at": "2025-08-08T10:00:00"
  }
]
```

---

## Food Tracking Endpoints

### Add Food Entry
**POST** `/food/`

Log food consumption.

**Request Body:**
```json
{
  "food_name": "Grilled Chicken Breast",
  "calories": 231,
  "meal_type": "lunch",
  "date": "2025-08-08"  // Optional, defaults to today
}
```

**Meal Types:** `breakfast`, `lunch`, `dinner`, `snack`

**Response:**
```json
{
  "id": 1,
  "date": "2025-08-08",
  "food_name": "Grilled Chicken Breast",
  "calories": 231,
  "meal_type": "lunch",
  "created_at": "2025-08-08T12:30:00"
}
```

### Get Food Entry
**GET** `/food/{entry_id}`

Retrieve a specific food entry.

### List Food Entries
**GET** `/food/`

Get all food entries, optionally filtered by date.

**Query Parameters:**
- `entry_date` (optional): Filter by date (YYYY-MM-DD)

**Example:** `/food/?entry_date=2025-08-08`

### Update Food Entry
**PUT** `/food/{entry_id}`

Update an existing food entry.

### Delete Food Entry
**DELETE** `/food/{entry_id}`

Remove a food entry.

---

## Water Tracking Endpoints

### Add Water Entry
**POST** `/water/`

Log water consumption.

**Request Body:**
```json
{
  "amount_ml": 500,
  "date": "2025-08-08"  // Optional, defaults to today
}
```

**Response:**
```json
{
  "id": 1,
  "date": "2025-08-08",
  "amount_ml": 500,
  "created_at": "2025-08-08T14:15:00"
}
```

### Get Water Entry
**GET** `/water/{entry_id}`

Retrieve a specific water entry.

### List Water Entries
**GET** `/water/`

Get all water entries, optionally filtered by date.

**Query Parameters:**
- `entry_date` (optional): Filter by date (YYYY-MM-DD)

### Update Water Entry
**PUT** `/water/{entry_id}`

Update water amount for an existing entry.

### Delete Water Entry
**DELETE** `/water/{entry_id}`

Remove a water entry.

---

## Progress & Analytics Endpoints

### Get Today's Progress
**GET** `/progress/`

Get current day progress with percentages and remaining amounts.

**Response:**
```json
{
  "date": "2025-08-08",
  "target_calories": 2000,
  "consumed_calories": 1456,
  "calories_percentage": 72.8,
  "remaining_calories": 544,
  "target_water_ml": 2500,
  "consumed_water_ml": 1750,
  "water_percentage": 70.0,
  "remaining_water_ml": 750,
  "food_entries": [
    {
      "id": 1,
      "food_name": "Grilled Chicken Breast",
      "calories": 231,
      "meal_type": "lunch",
      "created_at": "2025-08-08T12:30:00"
    }
  ],
  "water_entries": [
    {
      "id": 1,
      "amount_ml": 500,
      "created_at": "2025-08-08T14:15:00"
    }
  ]
}
```

### Get Progress for Specific Date
**GET** `/progress/{date}`

Get progress for any specific date.

**Parameters:**
- `date` (path): Date in YYYY-MM-DD format

### Get Nutrition Summary
**GET** `/summary/`

Get overall statistics across all tracked days.

**Response:**
```json
{
  "total_days_tracked": 15,
  "average_calories_percentage": 85.4,
  "average_water_percentage": 78.2,
  "days_met_calorie_goal": 12,
  "days_met_water_goal": 10
}
```

---

## Usage Examples

### Complete Daily Workflow

1. **Set daily goals:**
   ```bash
   curl -X POST "http://localhost:5000/goals/" \
     -H "Content-Type: application/json" \
     -d '{"target_calories": 2000, "target_water_ml": 2500}'
   ```

2. **Log breakfast:**
   ```bash
   curl -X POST "http://localhost:5000/food/" \
     -H "Content-Type: application/json" \
     -d '{"food_name": "Oatmeal with berries", "calories": 350, "meal_type": "breakfast"}'
   ```

3. **Log water:**
   ```bash
   curl -X POST "http://localhost:5000/water/" \
     -H "Content-Type: application/json" \
     -d '{"amount_ml": 500}'
   ```

4. **Check progress:**
   ```bash
   curl "http://localhost:5000/progress/"
   ```

### Python Client Example

```python
import requests
import json

BASE_URL = "http://localhost:5000"

# Set daily goal
goal_data = {"target_calories": 2000, "target_water_ml": 2500}
response = requests.post(f"{BASE_URL}/goals/", json=goal_data)
print("Goal set:", response.json())

# Add food
food_data = {"food_name": "Apple", "calories": 95, "meal_type": "snack"}
response = requests.post(f"{BASE_URL}/food/", json=food_data)
print("Food added:", response.json())

# Add water
water_data = {"amount_ml": 250}
response = requests.post(f"{BASE_URL}/water/", json=water_data)
print("Water added:", response.json())

# Check progress
response = requests.get(f"{BASE_URL}/progress/")
progress = response.json()
print(f"Calories: {progress['calories_percentage']}% complete")
print(f"Water: {progress['water_percentage']}% complete")
print(f"Remaining calories: {progress['remaining_calories']}")
print(f"Remaining water: {progress['remaining_water_ml']}ml")
```

## Error Handling

The API returns standard HTTP status codes:

- **200**: Success
- **404**: Resource not found
- **422**: Validation error
- **500**: Internal server error

**Error Response Format:**
```json
{
  "detail": "Error message description"
}
```

## Data Validation

- **Calories**: Must be >= 0
- **Water amount**: Must be > 0
- **Meal type**: Must be one of: breakfast, lunch, dinner, snack
- **Dates**: Automatically default to current date if not provided

## Development

### Running with Auto-reload
```bash
uvicorn main:app --host localhost --port 5000 --reload
```

### Environment Variables
- `DATABASE_URL`: Database connection string (optional, defaults to SQLite)

### Adding Features

The modular structure makes it easy to extend:
- Add new models in `models.py`
- Add new endpoints in `main.py`
- Modify database configuration in `database.py`

## Future Enhancements

Potential features to add:
- User authentication and multi-user support
- Notification service integration
- Food database with automatic calorie lookup
- Meal planning and recipe suggestions
- Export data functionality
- Mobile app integration
- Advanced analytics and charts

## License

This project is open source. Feel free to modify and distribute according to your needs.

## Support

For issues or questions:
1. Check the automatic API documentation at `/docs`
2. Review this README for usage examples
3. Examine the source code for implementation details

The API is designed to be simple, reliable, and easy to integrate with any frontend or mobile application.