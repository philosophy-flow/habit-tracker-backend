import uuid
from datetime import date
from app.db.session import SessionDep
from app.schemas.habit import HabitAdd, HabitUpdate
from app.models import HabitDB, HabitCompletionDB
from app.dependencies.sub import TokenDep
from app.utils.auth import get_user


def get_habits(db: SessionDep, token: TokenDep):
    user = get_user(token, db, "access")
    if not user:
        return False

    return user.habits


def create_habit(habit: HabitAdd, db: SessionDep, token: TokenDep):
    user = get_user(token, db, "access")
    if not user:
        return False

    habit_db = HabitDB(name=habit.name, user_id=user.user_id, frequency=habit.frequency)

    db.add(habit_db)
    db.commit()
    db.refresh(habit_db)

    return True


def delete_habit(habit_id: uuid.UUID, db: SessionDep, token: TokenDep):
    user = get_user(token, db, "access")
    if not user:
        return False

    habit = db.get(HabitDB, habit_id)
    if not habit or habit.user_id != user.user_id:
        return False

    db.delete(habit)
    db.commit()

    return True


def update_habit_complete(
    habit_id: uuid.UUID,
    date_completed: date,
    db: SessionDep,
    token: TokenDep,
):
    user = get_user(token, db, "access")
    if not user:
        return False

    habit_complete = db.get(HabitCompletionDB, (habit_id, date_completed))
    if not habit_complete:
        new_habit_complete = HabitCompletionDB(
            habit_id=habit_id, date_completed=date_completed
        )
        db.add(new_habit_complete)
        db.commit()
        db.refresh(new_habit_complete)

        return True
    else:
        db.delete(habit_complete)
        db.commit()

        return True


def update_habit_metadata(
    habit_id: uuid.UUID, updated_data: HabitUpdate, db: SessionDep, token: TokenDep
):
    user = get_user(token, db, "access")
    if not user:
        return False

    habit = db.get(HabitDB, habit_id)
    if not habit or habit.user_id != user.user_id:
        return False

    for key, value in updated_data:
        if value:
            setattr(habit, key, value)

    db.commit()
    db.refresh(habit)

    return True
