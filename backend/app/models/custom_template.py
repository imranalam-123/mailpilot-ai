from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from app.database.database import Base


class CustomTemplate(Base):

    __tablename__ = "custom_templates"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    name = Column(
        String,
        nullable=False
    )

    description = Column(
        String,
        nullable=False
    )

    sample_prompt = Column(
        String,
        nullable=False
    )