from typing import Optional
from datetime import date, datetime
from pydantic import root_validator
from sqlmodel import SQLModel, Field

class TimeLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int
    week_start_date: date
    monday_hours: int = Field(default=0)
    tuesday_hours: int = Field(default=0)
    wednesday_hours: int = Field(default=0)
    thursday_hours: int = Field(default=0)
    friday_hours: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    pto_hours: int = Field(default=0)

    @root_validator
    def check_total_hours(cls, values):
        """Ensure total worked hours from Monday through Friday equal 40."""
        total = (
                values.get("monday_hours", 0)
                + values.get("tuesday_hours", 0)
                + values.get("wednesday_hours", 0)
                + values.get("thursday_hours", 0)
                + values.get("friday_hours", 0)
        )
        if total != 40:
            raise ValueError("Total hours for the week must equal 40.")
        return values

    def __str__(self):
        return (
            f"TimeLog for employee {self.employee_id} starting on {self.week_start_date}:\n"
            f"  Monday: {self.monday_hours} hrs\n"
            f"  Tuesday: {self.tuesday_hours} hrs\n"
            f"  Wednesday: {self.wednesday_hours} hrs\n"
            f"  Thursday: {self.thursday_hours} hrs\n"
            f"  Friday: {self.friday_hours} hrs\n"
            f"Created at: {self.created_at}, PTO hours: {self.pto_hours}"
        )
