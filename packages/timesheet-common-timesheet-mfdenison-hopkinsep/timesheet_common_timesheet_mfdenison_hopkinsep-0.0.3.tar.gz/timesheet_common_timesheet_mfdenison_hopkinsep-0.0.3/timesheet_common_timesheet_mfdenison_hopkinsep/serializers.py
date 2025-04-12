from pydantic import BaseModel
from datetime import date, datetime

class TimeLogSerializer(BaseModel):
    id: int
    employee_id: int
    week_start_date: date
    monday_hours: int
    tuesday_hours: int
    wednesday_hours: int
    thursday_hours: int
    friday_hours: int
    pto_hours: int
    created_at: datetime

    class Config:
        orm_mode = True
