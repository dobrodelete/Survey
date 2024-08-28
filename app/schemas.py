from pydantic import BaseModel, Field, validator
from typing import List, Optional


class PunctModel(BaseModel):
    id: int
    title: str
    range_min: int
    range_max: int
    prompt: Optional[str]
    comment: Optional[str]

    class Config:
        orm_mode = True


class SubcriterionModel(BaseModel):
    id: int
    question_number: int
    title: str
    weight: float
    needed_answer: bool
    puncts: List[PunctModel] = []

    class Config:
        orm_mode = True


class CriterionModel(BaseModel):
    id: int
    title: str
    number: str
    subcriterions: List[SubcriterionModel] = []

    class Config:
        orm_mode = True


class DirectionModel(BaseModel):
    id: int
    title: str
    criterions: List[CriterionModel] = []

    class Config:
        orm_mode = True


class SurveyFormModel(BaseModel):
    directions: List[DirectionModel] = []

    @validator('directions', pre=True, always=True)
    def validate_directions(cls, v):
        if not v:
            raise ValueError('Survey must have at least one direction')
        return v
