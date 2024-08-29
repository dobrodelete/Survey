from typing import List, Optional, Any

from pydantic import BaseModel


class Punct(BaseModel):
    id: int
    title: str
    range_max: int
    range_min: int
    prompt: Any
    comment: Any
    subcriterion_id: int


class Subcriterion(BaseModel):
    id: int
    question_number: int
    title: str
    weight: float
    criterion_id: int
    # note: Optional[str]
    needed_answer: bool
    puncts: List[Punct]


class Criterion(BaseModel):
    id: int
    title: str
    number: str
    question_number: Optional[int] = None
    weight: Optional[float] = None
    question: Optional[Optional[str]] = None
    detailed_response: Optional[bool] = None
    direction_id: int
    subcriterions: List[Subcriterion]


class Direction(BaseModel):
    id: int
    title: str
    criterions: List[Criterion]


class Data(BaseModel):
    directions: List[Direction]


class Model(BaseModel):
    title_en: str
    title_ru: str
    version: int
    data: Data
