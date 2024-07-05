from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class DBVacancy(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(unique=True, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    employment: Mapped[str] = mapped_column(nullable=False)
    requirement: Mapped[str] = mapped_column(nullable=False)
    experience: Mapped[str] = mapped_column(nullable=False)
