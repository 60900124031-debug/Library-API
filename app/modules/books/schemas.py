from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    isbn: str = Field(min_length=10, max_length=20)
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    year: int | None = Field(default=None, ge=1000, le=2100)
    stock: int = Field(default=1, ge=0)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    author: str | None = Field(default=None, min_length=1, max_length=100)
    year: int | None = Field(default=None, ge=1000, le=2100)
    stock: int | None = Field(default=None, ge=0)


class BookResponse(BookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)