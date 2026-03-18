import enum
from app.core.database import Base
from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship


class DayOfWeek(str, enum.Enum):
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"


class OfficeHour(Base):
    __tablename__ = "office_hours"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(
        String(50),
        ForeignKey("employees.employee_code", ondelete="CASCADE"),
        nullable=False,
    )
    day_of_week = Column(Enum(DayOfWeek, name="day_of_week_enum"), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    employee = relationship("Employee", back_populates="office_hours")
