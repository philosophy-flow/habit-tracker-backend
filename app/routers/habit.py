from fastapi import APIRouter

from app.db.session import SessionDep

from app.schemas.habit import HabitAdd
from app.models.habit import HabitDB

router = APIRouter()


# create habit
@router.post("/create-habit")
def create_habit(habit: HabitAdd, db: SessionDep):
    habit_db = HabitDB(name=habit.name, user_id=habit.user_id)

    db.add(habit_db)
    db.commit()
    db.refresh(habit_db)

    return {"message": "Habit created.", "habit_id": habit_db.habit_id}


# delete habit

# edit habit
#    change name
#    toggle complete

# get all habits
