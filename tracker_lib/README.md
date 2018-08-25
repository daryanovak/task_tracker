##TaskTracker

The library tracker_lib contains the basic functionality for the creation of the organizer.

###The features of the library;
1. User authorization system
2. Work with one-time tasks
3. Work with periodic tasks
4. Access to the task to other users
5. Possibility to comment on the task be users
6. All tasks display
7. Tasks display by tags
8. Display of all tasks of the current user_id
9. Tasks display in a given interval
10. Superuser mode


###The structure of the library:
```
 ── tracker_lib
│   ├── lib
│   │   ├── controllers
│   │   │  
│   │   ├── helpers
│   │   │
│   │   ├── models
│   │   │  
│   │   ├── storage
│   │   │  
│   │   └── test_
``` 


####"controllers"  
The module contains three classes CommentController, TaskController, UserController, which contain fundamental functions for the work with TaskTrecker
  
####"helpers"  
The module contains supporting functionality for the library, for example, the setting of cron parser, supporting functions for the work with exceptions

####"models"  
The module contains the main models for the library work
  
####"storage"
The module for the work with database
  
####"test"  
Unit tests are created for the automatic check of the correct program work
  

###In order to use the library:  
For example, in order to import the class of TaskController from the module Controllers
```

import tracker_lib.lib.controllers.TaskController as task_controller
``` 
 
