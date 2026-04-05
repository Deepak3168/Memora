from schemas.log import LogCreate,LogResponse
from typing import Optional, List
from fastapi import Query

from utils.personal_logs import create_log,get_logs_by_day,remove_log
from db.db_sql import db
from fastapi import APIRouter,HTTPException



USER_ID =1 


log_router = APIRouter(prefix="/personal", tags=["Personal Logs"])

@log_router.post("/logs")
def create_log_api(payload: LogCreate):
    log_id = create_log(db, USER_ID, payload)
    return {
        "message": "Log created",
        "log_id": log_id
    }


@log_router.get("/logs", response_model=List[LogResponse])
def get_logs_api(day: Optional[str] = Query(None, description="YYYY-MM-DD")):
    return get_logs_by_day(db, USER_ID, day)


@log_router.delete("/logs/{log_id}")
def delete_log_api(log_id: int):
    success = remove_log(db, USER_ID, log_id)
    if not success:
        raise HTTPException(status_code=404, detail="Log not found")
    return {"message": "Log removed"}
