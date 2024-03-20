from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Integer, Column, String, create_engine, ForeignKey,Table

Base = declarative_base()
course_teacher = Table("course_teachers", Base.metadata, 
                       Column('course_id', ForeignKey('courses.id'), primary_key=True),
                       Column('teacher_id', ForeignKey('teachers.id'), primary_key=True),
                       extend_existing = True
                       )
class Student(Base):

    __tablename__ = "students"

    id = Column(Integer(), primary_key=True)
    real_first_name = Column(String())
    last_name = Column(String())
    age = Column(Integer())
    course_id = Column(Integer(), ForeignKey('courses.id'))

class Course(Base):

    __tablename__ = "courses"

    id = Column(Integer(), primary_key=True)
    course_name = Column(String())

    students = relationship('Student',backref="courses")
    teachers = relationship("Teacher", secondary=course_teacher, back_populates='courses')

class Teacher(Base):

    __tablename__ = "teachers"

    id = Column(Integer(), primary_key=True)
    teacher_name = Column(String())

    courses = relationship("Course", secondary=course_teacher, back_populates="teachers")


if __name__ == '__main__':
    engine = create_engine('sqlite:///students.db')
    Base.metadata.create_all(engine)

    sessionmade = sessionmaker(bind=engine)
    session = sessionmade()

    # students = session.query(Student).filter(Student.id == 3)
    students = session.query(Student).filter_by(last_name="Good Student")
    print([student.last_name for student in students.all()])

    student1 = Student(real_first_name="Student", age=20, last_name="Good Student", course_id=1)
    session.add(student1)
    course1 = Course(course_name="Software Engineering")
    session.add(course1)
    teacher1 = Teacher(teacher_name="Mercy Nzau")
    session.add(teacher1)
    teacher1.courses.append(course1)
    session.commit()

    print(session.get(Student,3).courses.course_name)
    print("Course Teachers for 5th course", session.get(Course,5).teachers)


# student1 = Student("Mercy",20)
# print(student1.name)