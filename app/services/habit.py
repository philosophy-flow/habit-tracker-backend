import uuid
from typing import Optional
from app.db.session import SessionDep
from app.schemas.habit import HabitAdd, HabitResponse
from app.models import HabitDB
from app.dependencies.sub import TokenDep
from app.utils.auth import get_user


def create_habit(habit: HabitAdd, db: SessionDep, token: TokenDep) -> Optional[HabitDB]:
    active_user = get_user(token, db, "access")
    if not active_user:
        return None

    habit_db = HabitDB(name=habit.name, user_id=active_user.user_id)
    active_user.habits.append(habit_db)

    db.commit()
    db.refresh(habit_db)

    return habit_db


def delete_habit(habit_id: uuid.UUID, db: SessionDep, token: TokenDep):
    user = get_user(token, db, "access")
    print(user)
    if not user:
        return False

    habits = [habit for habit in user.habits if habit_id != habit.habit_id]
    user.habits = habits

    db.commit()

    return True
