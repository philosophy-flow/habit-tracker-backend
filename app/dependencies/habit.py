from typing import Annotated
from fastapi import Depends

from app.schemas.habit import HabitResponse
from app.services.habit import create_habit


CreateDep = Annotated[HabitResponse, Depends(create_habit)]
