from pydantic import BaseModel


class _BaseModel(BaseModel):
    class Config:
        orm_mode = True


class DirectorSchema(_BaseModel):
    id: int
    name: str


class MovieSchema(_BaseModel):
    id: int
    imdb_id: str
    title: str
    year: int
    image_url: str
    imdb_rating: float
    imdb_rating_count: str

    director: DirectorSchema
