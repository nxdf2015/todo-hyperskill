
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer,String,Date,Column
from sqlalchemy.orm import sessionmaker
from datetime import datetime,timedelta

#TODO create database and table task( id primary key, task string, deadline date)
engine = None

Base = declarative_base()

class TodoModel(Base):
    __tablename__='task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __str__(self):
        return self.task


def create(namebase = 'todo.db'):
    global engine
    if engine == None:
        url = f'sqlite:///{namebase}?check_name=False'
        engine = create_engine(url)
        Base.metadata.create_all(engine)


create()


def  getDayWeek(today = datetime.today()):
    i= 0
    while i < 7:
        yield (today + timedelta(days=i)).date()
        i+=1

def getDate(datestring , format = "%Y-%m-%d"):
    return datetime.strptime(datestring,format)

def formatDate(date, dayName = False):
    if dayName:
        format = "%A %d %b"
    else:
        format = "%Y-%m-%d"


    return date.strftime(format)


class TodoApp:
    Session = sessionmaker(bind = engine)

    def __init__(self):

        self.session = TodoApp.Session()




    def menu(self):
        while True:
            print("1) Today's tasks")
            print("2) Week's tasks")
            print("3) All tasks")
            print("4) Missed tasks")
            print("5) Add task")
            print("6) Delete task")
            print("0) Exit")
            choice = int(input())

            if choice == 1:
                row = self.getTodayTask()

                self.render_todo(row)
            elif choice == 2:
                self.getWeekTask()
            elif choice == 3:
                self.getAllTask()
            elif choice == 4:
                self.getMissedTask()
            elif choice == 5:
                self.addTask()
            elif choice == 6:
                self.deleteTask()
            else:
                break
        print("Bye!")

    def getWeekTask(self):
        today = datetime.today()
        seven_days = timedelta(days=8)
        for date_day in getDayWeek():
            row = self.getTodayTask(date_day)
            self.render_todo(row,date_day,dayName=True)

    def getAllTask(self,number=False):
        rows = self.session.query(TodoModel).all()
        print("Today:")
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            i = 0
            for row in rows:
                if number:
                    print(f"{i}. {row.task} {row.deadline.strftime('%d %m')}")
                print(row)



    def addTask(self):
        print("Enter a task")
        task = input()
        print("Enter deadline")
        date = getDate(input())
        row = TodoModel(task= task,deadline = date )
        self.session.add(row)
        self.session.commit()
        print("The task has been added!")

    def getTodayTask(self,date = datetime.today()):
        row = self.session.query(TodoModel).filter(TodoModel.deadline == date).all()
        return row


    def render_todo(self,rows,date=datetime.today(),dayName = False):
        print(formatDate(date,dayName))
        if  rows  == []  :
                print("Nothing to do!")
        else:
            for id, row in enumerate(rows ):
                print(f"{id}. {row.task}")
        print()

    def getMissedTask(self):
        today = datetime.today()
        rows = self.session.query(TodoModel).filter( TodoModel.deadline < today).all()
        print("Missed tasks:")
        self.render_todo(rows)

    def deleteTask(self):
        self.getAllTask(number=True)
        print("Choose the number of the task you want to delete:")
        id = int(input())
        self.session.query(TodoModel).filter(TodoModel.id==id).delete()
        self.session.commit()
        print("The task has been deleted!")





todoapp = TodoApp()
todoapp.menu()


# 1) Do yoga
# 2) Make breakfast
# 3) Learn basics of SQL
# 4) Learn what is ORM""")
