from fastapi import FastAPI, HTTPException, Depends, Header, status
from sqlmodel import Session, select
from database import create_db_and_tables, get_session, OffsetDump
from pydantic import BaseModel
import os
from typing import Dict, Any

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CS2-Central API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MASTER_KEY = os.getenv("MASTER_KEY")
if not MASTER_KEY:
    raise RuntimeError("MASTER_KEY environment variable is not set")

async def verify_key(x_api_key: str = Header(...)):
    if x_api_key != MASTER_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )


class DumpUpload(BaseModel):
    filename: str
    content: Dict[str, Any]
    hash: str

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/upload", status_code=status.HTTP_201_CREATED)
def upload_dump(
    dump: DumpUpload,
    session: Session = Depends(get_session),
    authorized: bool = Depends(verify_key)
):

    
    new_dump = OffsetDump(
        filename=dump.filename,
        content=dump.content,
        hash=dump.hash
    )
    session.add(new_dump)
    session.commit()
    session.refresh(new_dump)
    return {"id": new_dump.id, "status": "uploaded"}

@app.get("/latest/{filename}")
def get_latest_dump(filename: str, session: Session = Depends(get_session)):
    statement = select(OffsetDump).where(OffsetDump.filename == filename).order_by(OffsetDump.created_at.desc())
    result = session.exec(statement).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="File not found")
        
    return result.content

@app.get("/")
def read_root():
    return {"message": "CS2-Central API is running"}
