import uuid
from typing import Optional
from fastapi import APIRouter, HTTPException

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

    return habit_db


# delete habit
@router.delete("/delete-habit/{habit_id}")
def delete_habit(habit_id: uuid.UUID, db: SessionDep):
    habit = db.get(HabitDB, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found.")

    db.delete(habit)
    db.commit()
    return {"message": "Habit deleted."}


# edit habit
#    change name
#    toggle complete

# get all habits
