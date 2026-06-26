from pydantic import BaseModel


class CustomTemplateCreate(BaseModel):
    name: str
    description: str
    sample_prompt: str


class CustomTemplateUpdate(BaseModel):
    name: str
    description: str
    sample_prompt: str