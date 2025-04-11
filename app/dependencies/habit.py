from typing import Annotated, List
from fastapi import Depends

from app.services.habit import (
    get_habits,
    create_habit,
    delete_habit,
    update_habit_complete,
    update_habit_metadata,
)
from app.schemas.habit import HabitResponseFlat

GetDep = Annotated[List[HabitResponseFlat], Depends(get_habits)]
CreateDep = Annotated[bool, Depends(create_habit)]
DeleteDep = Annotated[bool, Depends(delete_habit)]
CompleteDep = Annotated[bool, Depends(update_habit_complete)]
UpdateDep = Annotated[bool, Depends(update_habit_metadata)]
