from pydantic import BaseModel


class TemplateResponse(BaseModel):
    name: str
    title: str