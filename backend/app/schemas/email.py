from pydantic import BaseModel, EmailStr
from enum import Enum


class EmailType(str, Enum):
    leave = "leave"
    meeting = "meeting"
    job_application = "job_application"


class Tone(str, Enum):
    formal = "formal"
    friendly = "friendly"
    professional = "professional"


class Template(str, Enum):
    sick_leave = "sick_leave"
    casual_leave = "casual_leave"
    resignation = "resignation"
    complaint = "complaint"
    meeting_request = "meeting_request"
    internship_request = "internship_request"
    job_application = "job_application"
    follow_up = "follow_up"
    thank_you = "thank_you"


class EmailRequest(BaseModel):
    email_type: EmailType
    tone: Tone
    template: Template
    prompt: str


class SendEmailRequest(BaseModel):
    to_email: EmailStr
    subject: str
    body: str


class GenerateAndSendRequest(BaseModel):
    to_email: EmailStr
    email_type: EmailType
    tone: Tone
    template: Template
    prompt: str