from pydantic import BaseModel, Field

# end-points will throw this whenever it encountered any exceptions.


class RFC7807ExceptionModel(BaseModel):
    title: str = Field(description="Summary of the exception")
    detail: str = Field(description="Detailed description of the exception")
    status: int = Field(description="HTTP status code")
