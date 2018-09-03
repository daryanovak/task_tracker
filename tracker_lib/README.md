##TaskTracker

The library tracker_lib contains the basic functionality for the creation of the organizer.

###The features of the library:
1. Work with one-time tasks
3. Work with periodic tasks
4. Share permission to the task to other users
5. Possibility to comment task
6. Get all tasks subtasks
7. Tasks display by tags
8. Get all tasks of the current user_id
9. Tasks display in a given interval
10. Edit task parameters

###Install:
You should go to tracker_lib directory and 
```
python3.6 setup.py install
```

###The structure of the library:
```
 ── tracker_lib
│   ├────
│   │   ├── controllers
│   │   │  
│   │   ├── helpers
│   │   │
│   │   ├── storage
│   │     
│   ├── models
``` 


####"controllers"  
The module contains three classes CommentController, TaskController, which contain fundamental functions for the work
with TaskTracker
  
####"helpers"  
The module contains supporting functionality for the library, for example, the setting of cron parser, supporting 
functions for the work with exceptions

####"models"  
The module contains the main models for the library work
  
####"storage"
The module for the work with database postgres (PonyORM)
  
####"test"  
Unit tests are created for the automatic check of the correct program work
  

###In order to use the library:  
For example, in order to import the class of TaskController from the module Controllers
```

from tracker_lib.controllers.task import TaskController

controller = TaskController(user_id = 1)

controller.create_task("title", "text", 1)

``` 
 
##Running the tests
How to run the automated tests for this system?
```
python3.6 -m unittest discover

```
