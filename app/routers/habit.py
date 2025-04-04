from fastapi import APIRouter, HTTPException
from app.dependencies.habit import CreateDep, DeleteDep


router = APIRouter()


# create habit
@router.post("/create-habit")
def create_habit(habit: CreateDep):
    return habit


# delete habit
@router.delete("/delete-habit/{habit_id}")
def delete_habit(success: DeleteDep):
    if not success:
        raise HTTPException(status_code=404, detail="Habit not found.")

    return {"message": "Habit deleted."}


# edit habit
#    change name
#    toggle complete

# get all habits
