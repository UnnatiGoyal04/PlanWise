from fastapi import APIRouter
router=APIRouter()
@router.get("/")
def home():
    return {"Message": "Welcome to PlanWise!"}
@router.get("/about")
def about():
    return{
        "project": "PlanWise",
        "version": "0.1.0",
        "status": "Development"
    }