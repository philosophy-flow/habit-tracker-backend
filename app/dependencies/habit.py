from typing import Annotated
from fastapi import Depends

from app.services.habit import create_habit, delete_habit, update_habit_complete

CreateDep = Annotated[bool, Depends(create_habit)]
DeleteDep = Annotated[bool, Depends(delete_habit)]
CompleteDep = Annotated[bool, Depends(update_habit_complete)]
