import uuid
from typing import Optional
from app.db.session import SessionDep
from app.schemas.habit import HabitAdd, HabitResponse
from app.models import HabitDB
from app.dependencies.sub import TokenDep
from app.utils.auth import get_user


def create_habit(habit: HabitAdd, db: SessionDep, token: TokenDep):
    active_user = get_user(token, db, "access")
    if not active_user:
        print("User not found")
        return False

    habit_db = HabitDB(name=habit.name, user_id=active_user.user_id)

    db.add(habit_db)
    db.commit()
    db.refresh(habit_db)

    return True


def delete_habit(habit_id: uuid.UUID, db: SessionDep, token: TokenDep):
    user = get_user(token, db, "access")
    habit = db.get(HabitDB, habit_id)
    if not habit or not user or habit.user_id != user.user_id:
        return False

    db.delete(habit)
    db.commit()

    return True
