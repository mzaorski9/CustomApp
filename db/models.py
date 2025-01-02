from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from sqlalchemy import String, Integer, Numeric, ForeignKey



class Base(DeclarativeBase):
    ...
# mapping an object to a table (mapped_column is the modern way sqlalchemy ORM does it)   
class Candidates(Base):
    __tablename__ = "candidates"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    adress1: Mapped[str] = mapped_column(String(50))
    adress2: Mapped[str] = mapped_column(String(50))
    city: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    state: Mapped[str] = mapped_column(String(30))
    zip_code: Mapped[int] = mapped_column(Integer)
    # establish relationships with Jobs; relation is bidirectional ('one to many'); through black_populates 
    # SQLAlchemy keeps related sides in sync (relationship(..., black_populates=...) must
    # be specified in both classes, and must point on each other);
    # 'many to one': job: Mapped["Jobs"] = relationship()
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), nullable=False)
    job: Mapped["Jobs"] = relationship("Jobs", back_populates="candidates")

class Jobs(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    position: Mapped[str] = mapped_column(String(50), nullable=False)
    type: Mapped[str] = mapped_column(String(10), nullable=False)
    location: Mapped[str] = mapped_column(String(30), nullable=False)
    salary: Mapped[str] = mapped_column(Numeric(10), nullable=False)
    description: Mapped[str] = mapped_column(String(2500))
    
    candidates: Mapped[list["Candidates"]] = relationship("Candidates", back_populates="job")

