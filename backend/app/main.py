from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def home():
    return {"message": "Welcome to PlanWise!"}
@app.get("/about")
def about():
    return{
        "project": "PlanWise",
        "version": "0.1.0",
        "status": "Development"
    }