from fastapi import APIRouter
from app.dependencies.habit import CreateDep


router = APIRouter()


# create habit
@router.post("/create-habit")
def create_habit(habit: CreateDep):
    return habit


# delete habit
# @router.delete("/delete-habit/{habit_id}")
# def delete_habit(habit_id: uuid.UUID, db: SessionDep, token: TokenDep):
#     habit = db.get(HabitDB, habit_id)
#     if not habit:
#         raise HTTPException(status_code=404, detail="Habit not found.")

#     db.delete(habit)
#     db.commit()
#     return {"message": "Habit deleted."}


# edit habit
#    change name
#    toggle complete

# get all habits
