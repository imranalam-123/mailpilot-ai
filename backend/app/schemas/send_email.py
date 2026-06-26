from pydantic import BaseModel, EmailStr


class SendEmailRequest(BaseModel):
    to_email: EmailStr
    subject: str
    body: str