from sqlalchemy import func

from fastapi import (
    FastAPI,
    Depends,
    HTTPException
)

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.database.database import (
    engine,
    get_db
)

from app.models.user import User
from app.models.email_history import EmailHistory

from app.schemas.user import UserCreate

from app.schemas.email import (
    EmailRequest,
    GenerateAndSendRequest
)

from app.schemas.send_email import (
    SendEmailRequest
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.core.dependencies import (
    get_current_user
)

from app.services.gemini_service import (
    generate_email
)

from app.services.email_service import (
    send_email
)

from app.models.custom_template import (
    CustomTemplate
)

from app.schemas.custom_template import (
    CustomTemplateCreate
)

from app.schemas.custom_template import (
    CustomTemplateCreate,
    CustomTemplateUpdate
)

from app.models.custom_template import (
    CustomTemplate
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MailPilot AI"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

User.metadata.create_all(bind=engine)
EmailHistory.metadata.create_all(bind=engine)
CustomTemplate.metadata.create_all(bind=engine)

# ==========================
# CREATE TABLES
# ==========================

User.metadata.create_all(bind=engine)
EmailHistory.metadata.create_all(bind=engine)



# ==========================
# HOME
# ==========================

@app.get("/")
def home():
    return {
        "message": "MailPilot AI Running"
    }


# ==========================
# REGISTER
# ==========================

@app.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User Registered Successfully",
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    }


# ==========================
# LOGIN
# ==========================

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="Invalid Email or Password"
        )

    if not verify_password(
        form_data.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid Email or Password"
        )

    access_token = create_access_token(
        data={
            "sub": db_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ==========================
# CURRENT USER
# ==========================

@app.get("/me")
def read_current_user(
    current_user: dict = Depends(
        get_current_user
    )
):
    return {
        "current_user": current_user
    }


# ==========================
# GENERATE EMAIL
# ==========================

@app.post("/generate-email")
def generate_email_endpoint(
    request: GenerateAndSendRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == current_user["email"]
    ).first()

    recipient_name = (
        request.to_email
        .split("@")[0]
        .replace(".", " ")
        .replace("_", " ")
        .title()
    )

    generated_email = generate_email(
        db_user.name,
        recipient_name,
        request.email_type.value,
        request.tone.value,
        request.template.value,
        request.prompt
    )

    new_email = EmailHistory(
        user_id=db_user.id,
        email_type=request.email_type.value,
        prompt=request.prompt,
        generated_email=generated_email
    )

    db.add(new_email)
    db.commit()
    db.refresh(new_email)

    return {
        "recipient": request.to_email,
        "subject": f"{request.email_type.value.title()} Email",
        "generated_email": generated_email
    }

# ==========================
# EMAIL HISTORY
# ==========================

@app.get("/email-history")
def get_email_history(
    current_user: dict = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == current_user["email"]
    ).first()

    emails = db.query(
        EmailHistory
    ).filter(
        EmailHistory.user_id == db_user.id
    ).order_by(
        EmailHistory.id.desc()
    ).all()

    return emails


# ==========================
# SEND EMAIL
# ==========================

@app.post("/send-email")
def send_email_endpoint(
    request: SendEmailRequest,
    current_user: dict = Depends(
        get_current_user
    )
):

    result = send_email(
        request.to_email,
        request.subject,
        request.body
    )

    return result


# ==========================
# GENERATE AND SEND EMAIL
# ==========================

@app.post("/generate-and-send-email")
def generate_and_send_email(
    request: GenerateAndSendRequest,
    current_user: dict = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == current_user["email"]
    ).first()

    recipient_name = (
    request.to_email
    .split("@")[0]
    .split(".")[0]
    .split("_")[0]
    .capitalize()
)

    generated_email = generate_email(
        db_user.name,
        recipient_name,
        request.email_type.value,
        request.tone.value,
        request.template.value,
        request.prompt
    )

    new_email = EmailHistory(
        user_id=db_user.id,
        email_type=request.email_type.value,
        prompt=request.prompt,
        generated_email=generated_email
    )

    db.add(new_email)
    db.commit()
    db.refresh(new_email)

    smtp_result = send_email(
        request.to_email,
        f"{request.email_type.value.title()} Email",
        generated_email
    )

    return {
        "message": "Email generated and sent successfully",
        "to_email": request.to_email,
        "sender_name": db_user.name,
        "recipient_name": recipient_name,
        "email_id": new_email.id,
        "generated_email": generated_email,
        "smtp_result": smtp_result
    }

# ==========================
# EMAIL TEMPLATES
# ==========================

@app.get("/email-templates")
def get_email_templates():

    templates = [
        {
            "name": "sick_leave",
            "title": "Sick Leave"
        },
        {
            "name": "casual_leave",
            "title": "Casual Leave"
        },
        {
            "name": "resignation",
            "title": "Resignation"
        },
        {
            "name": "complaint",
            "title": "Complaint"
        },
        {
            "name": "meeting_request",
            "title": "Meeting Request"
        },
        {
            "name": "internship_request",
            "title": "Internship Request"
        },
        {
            "name": "job_application",
            "title": "Job Application"
        },
        {
            "name": "follow_up",
            "title": "Follow Up"
        },
        {
            "name": "thank_you",
            "title": "Thank You"
        }
    ]

    return {
        "templates": templates
    }

# ==========================
# TEMPLATE DETAILS
# ==========================

@app.get("/email-templates/{template_name}")
def get_template_details(
    template_name: str
):

    templates = {
        "sick_leave": {
            "title": "Sick Leave",
            "description": "Request leave because of illness",
            "sample_prompt": "I have fever and need 2 days leave"
        },

        "casual_leave": {
            "title": "Casual Leave",
            "description": "Request personal leave",
            "sample_prompt": "I need leave for a family function"
        },

        "resignation": {
            "title": "Resignation",
            "description": "Resignation from current company",
            "sample_prompt": "I am resigning due to higher studies"
        },

        "complaint": {
            "title": "Complaint",
            "description": "Professional complaint email",
            "sample_prompt": "Internet service is not working"
        },

        "meeting_request": {
            "title": "Meeting Request",
            "description": "Request a meeting",
            "sample_prompt": "Need a project discussion meeting"
        },

        "internship_request": {
            "title": "Internship Request",
            "description": "Request internship opportunity",
            "sample_prompt": "Seeking summer internship opportunity"
        },

        "job_application": {
            "title": "Job Application",
            "description": "Apply for a job opening",
            "sample_prompt": "Applying for Python Developer role"
        },

        "follow_up": {
            "title": "Follow Up",
            "description": "Follow up on previous communication",
            "sample_prompt": "Following up on my interview status"
        },

        "thank_you": {
            "title": "Thank You",
            "description": "Professional thank you email",
            "sample_prompt": "Thank you for conducting the interview"
        }
    }

    if template_name not in templates:
        raise HTTPException(
            status_code=404,
            detail="Template not found"
        )

    return templates[template_name]

# ==========================
# SAVE CUSTOM TEMPLATE
# ==========================

@app.post("/save-template")
def save_template(
    request: CustomTemplateCreate,
    current_user: dict = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == current_user["email"]
    ).first()

    new_template = CustomTemplate(
        user_id=db_user.id,
        name=request.name,
        description=request.description,
        sample_prompt=request.sample_prompt
    )

    db.add(new_template)
    db.commit()
    db.refresh(new_template)

    return {
        "message": "Template Saved Successfully",
        "template_id": new_template.id,
        "name": new_template.name
    }

# ==========================
# MY TEMPLATES
# ==========================

@app.get("/my-templates")
def get_my_templates(
    current_user: dict = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == current_user["email"]
    ).first()

    templates = db.query(
        CustomTemplate
    ).filter(
        CustomTemplate.user_id == db_user.id
    ).all()

    return templates

# ==========================
# GET SINGLE TEMPLATE
# ==========================

@app.get("/my-templates/{template_id}")
def get_template(
    template_id: int,
    current_user: dict = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == current_user["email"]
    ).first()

    template = db.query(
        CustomTemplate
    ).filter(
        CustomTemplate.id == template_id,
        CustomTemplate.user_id == db_user.id
    ).first()

    if not template:
        raise HTTPException(
            status_code=404,
            detail="Template not found"
        )

    return template

# ==========================
# UPDATE TEMPLATE
# ==========================

@app.put("/my-templates/{template_id}")
def update_template(
    template_id: int,
    request: CustomTemplateUpdate,
    current_user: dict = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == current_user["email"]
    ).first()

    template = db.query(
        CustomTemplate
    ).filter(
        CustomTemplate.id == template_id,
        CustomTemplate.user_id == db_user.id
    ).first()

    if not template:
        raise HTTPException(
            status_code=404,
            detail="Template not found"
        )

    template.name = request.name
    template.description = request.description
    template.sample_prompt = request.sample_prompt

    db.commit()
    db.refresh(template)

    return {
        "message": "Template Updated Successfully",
        "id": template.id,
        "name": template.name,
        "description": template.description,
        "sample_prompt": template.sample_prompt
    }

# ==========================
# DELETE TEMPLATE
# ==========================

@app.delete("/my-templates/{template_id}")
def delete_template(
    template_id: int,
    current_user: dict = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == current_user["email"]
    ).first()

    template = db.query(
        CustomTemplate
    ).filter(
        CustomTemplate.id == template_id,
        CustomTemplate.user_id == db_user.id
    ).first()

    if not template:
        raise HTTPException(
            status_code=404,
            detail="Template not found"
        )

    db.delete(template)
    db.commit()

    return {
        "message": "Template Deleted Successfully",
        "deleted_template_id": template_id
    }

# ==========================
# USER STATS
# ==========================

@app.get("/stats")
def get_stats(
    current_user: dict = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == current_user["email"]
    ).first()

    total_emails_generated = db.query(
        EmailHistory
    ).filter(
        EmailHistory.user_id == db_user.id
    ).count()

    total_custom_templates = db.query(
        CustomTemplate
    ).filter(
        CustomTemplate.user_id == db_user.id
    ).count()

    most_used_type = db.query(
        EmailHistory.email_type,
        func.count(
            EmailHistory.email_type
        ).label("count")
    ).filter(
        EmailHistory.user_id == db_user.id
    ).group_by(
        EmailHistory.email_type
    ).order_by(
        func.count(
            EmailHistory.email_type
        ).desc()
    ).first()

    return {
        "user": db_user.name,
        "email": db_user.email,
        "total_emails_generated":
            total_emails_generated,
        "total_custom_templates":
            total_custom_templates,
        "most_used_email_type":
            most_used_type[0]
            if most_used_type
            else None
    }