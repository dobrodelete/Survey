from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class AdminBase(BaseModel):
    name: str


class AdminCreate(AdminBase):
    password: str


class AdminRead(AdminBase):
    id: int


class IogvBase(BaseModel):
    hierarchy_id: str
    depth_level: int
    name: str
    parent_id: Optional[str] = None


class IogvCreate(IogvBase):
    pass


class IogvRead(IogvBase):
    pass


class UserBase(BaseModel):
    post: str
    iogv_id: Optional[str] = None
    subdivision_id: Optional[str] = None
    person_id: Optional[str] = None
    created_at: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int


class RecordBase(BaseModel):
    uid: int
    responce_time: Optional[str] = None
    created_at: str


class RecordCreate(RecordBase):
    pass


class RecordRead(RecordBase):
    id: int


class AnswerBase(BaseModel):
    rid: int
    number_question: int
    answer: float
    comment: Optional[str] = None


class AnswerCreate(AnswerBase):
    pass


class AnswerRead(AnswerBase):
    pass


class ReportBase(BaseModel):
    iogv: str
    subdv: str
    post: str
    created_at: str
    link: str
    record_id: int


class ReportCreate(ReportBase):
    pass


class ReportRead(ReportBase):
    id: int
