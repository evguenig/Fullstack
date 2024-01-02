from sqlalchemy import (
    create_engine, ForeignKey, Column, Integer, String
)
from sqlalchemy.orm import registry, relationship, Session

engine = create_engine("postgresql+psycopg2://myuser:mypassword@localhost/project_tracker", echo=True)

mapper_registry = registry()
Base = mapper_registry.generate_base()


class Project(Base):
    __tablename__ = 'projects'

    project_id = Column(Integer, primary_key=True)
    title = Column(String(length=50))

    def __repr__(self):
        return f"<Project(id={self.project_id}, title={self.title})>"


class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.project_id'))
    description = Column(String(length=50))

    project = relationship("Project")

    def __repr__(self):
        return f"<Task(task_id={self.task_id}, description ={self.description}, project_id={self.project_id})>"


# Create all tables
Base.metadata.create_all(engine)

with Session(engine) as session:
    clean_house_project = Project(title="Clean house")
    session.add(clean_house_project)
    session.flush()

    task = Task(description="Clean bedroom", project_id=clean_house_project.project_id)
    session.add(task)
    session.commit()
