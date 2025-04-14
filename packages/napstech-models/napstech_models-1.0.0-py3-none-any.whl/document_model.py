import pydantic # type: ignore
from typing import Optional, List
from pydantic import BaseModel, Field # type: ignore
from datetime import datetime,timezone



class tasklist(BaseModel):
    task_id: str = Field(..., description="Task ID")
    task_name: str = Field(..., description="Task name")
    task_status: str = Field(..., description="Task status")
    task_type: str = Field(..., description="Task type")
    task_description: str = Field(..., description="Task description")
    task_created_at: datetime = Field(default_factory=lambda : datetime.now(timezone.utc), description="Task creation timestamp")
    task_updated_at: datetime = Field(default_factory=lambda : datetime.now(timezone.utc), description="Task update timestamp")
    task_completed_at: Optional[datetime] = Field(default=lambda : datetime.now(timezone.utc), description="Task completion timestamp")
    task_result_id: Optional[str] = Field(default=None, description="Task result")
    task_log_id: Optional[str] = Field(default=None, description="Task error message")

class PageList(BaseModel):
    page_id: str = Field(..., description="Page ID")
    page_number: int = Field(default=0, description="Page number")
    page_index: int = Field(default=0, description="Page index")
    page_s3_path: str = Field(..., description="S3 path for the page")
    task_list:List[tasklist] = Field(default=[], description="List of tasks associated with the page")    

class Document(BaseModel):
    id:str = Field(default=None, description="Unique Job ID")
    document_id: str = Field(..., description="Document ID")
    total_pages : int = Field(default=0, description="Total number of pages in the document")
    page_list: List[PageList] = Field(default=[], description="List of pages in the document")
    created_at: datetime = Field(default_factory=lambda : datetime.now(timezone.utc), description="Creation timestamp")
    steps_list: List[tasklist] = Field(default=[], description="List of steps in the document processing pipeline")
class request_model(BaseModel):
    job_id: str = Field(..., description="Unique Job ID")
    document_id: str = Field(..., description="Document ID")
    
