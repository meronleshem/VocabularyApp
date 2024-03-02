from Database.DatabaseManager import *
from View.View import ViewManager
from Controllers.AppController import AppController

if __name__ == '__main__':

    db = DatabaseManager()
    view = ViewManager()

    controller = AppController(db, view)

    view.mainloop()

    db.close_db_connection()

