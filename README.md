# TaskTracker
TaskTracker is meant to be a dead simple text based task manager. There are many task managers out there. What makes TaskTraker different? 
First of all,it manages multiple types of tasks(single or periodic), creates subtasks, assigns project members to tasks, comments on tasks, assigns project specific tags to tasks and much more. Using Python3.

## Structure
####Library
tracker_lib is a core of TaskTracker. All activities about managing tasks, users and projects located inside of core.

You can use library to create your own task tracker, organizer, TODO-list, etc. Library provides base to create your own app by adding features over it.

See tasktracker_lib package.

####Console
You can use console part to try core in action. Console part lets you test features easily.

See tasktracker_console package.

## Getting Started
####How to use - tracker_lib
For import package:
```
import tracker_lib.lib.controllers.TaskController as task_controller
task = task_controller.create_task(param,....) 
```

####How to use - Console
First of all you should authenticate user_id,
whose login will be used to perform actions

```
 sign_up user_id password
 log_in user_id password
```
Now you can start use to console version of TaskTracker. For example, create task:
```
 create_task title1 text1 0 --tags "example,tutorial"
```


##Running the tests
How to run the automated tests for this system?
```
python3.6 ./todo_mvc/run_test.py

```
##Contributing
Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.






