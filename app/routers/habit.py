from fastapi import APIRouter, HTTPException

from app.dependencies.habit import CreateDep, DeleteDep


router = APIRouter()


# create habit
@router.post("/create-habit")
def create_habit(success: CreateDep):
    if not success:
        raise HTTPException(status_code=404, detail="Could not create habit.")

    return {"message": "Habit created."}


# delete habit
@router.delete("/delete-habit/{habit_id}")
def delete_habit(success: DeleteDep):
    if not success:
        raise HTTPException(status_code=404, detail="Habit not found.")

    return {"message": "Habit deleted."}


# handles completion toggles, modifies habit_completion table
# @router.put("/update-habit/{habit_id}/completions/{date}")
# def update_habit_completions():
#     print("Updating completion")
