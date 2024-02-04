from pydantic import BaseModel, Field


class UserDataModelResponse(BaseModel):
    status: str = Field(description="Status of the response")
    inserted_id: str = Field(description="inserted id no in database")
