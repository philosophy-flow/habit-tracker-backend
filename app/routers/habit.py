from fastapi import APIRouter, HTTPException

from app.dependencies.habit import GetDep, CreateDep, DeleteDep, CompleteDep, UpdateDep


router = APIRouter()


@router.get("/get-habits")
def get_habits(habits: GetDep):
    if not isinstance(habits, list):
        raise HTTPException(status_code=500, detail="Could not get habits.")

    return habits


@router.post("/create-habit")
def create_habit(success: CreateDep):
    if not success:
        raise HTTPException(status_code=500, detail="Could not create habit.")

    return {"message": "Habit created."}


@router.delete("/delete-habit/{habit_id}")
def delete_habit(success: DeleteDep):
    if not success:
        raise HTTPException(status_code=404, detail="Habit not found.")

    return {"message": "Habit deleted."}


@router.put("/update-habit/{habit_id}/completions/{date_completed}")
def update_habit_completions(success: CompleteDep):
    if not success:
        raise HTTPException(
            status_code=500, detail="Unable to update habit completion status."
        )

    return {"message": f"Habit completion status updated."}


@router.patch("/update-habit/{habit_id}")
def update_habit_metadata(success: UpdateDep):
    if not success:
        raise HTTPException(status_code=500, detail="Unable to update habit metadata.")

    return {"message": "Habit metadata updated."}
