#Commanline commands:
#TASK  
####create a new single task  

```
todo create_task title text 1 --tags "example"
```


positional arguments:  
-title   
-text   
-status 

optional arguments:  
--tags   
--parent_title    
--date

####create a new periodic task   

#### 
```
todo create_periodic_task title text 1 "01/01/01 00:00" "02/02/02 00:00"
```
 
positional arguments:  
-title   
-text   
-status 

optional arguments:  
--tags   
--parent_title  
--date_start  
--deadline 
--period 

####get all user tasks 
#### 
```
todo get_tasks    
```


#### get task by id    
``` 
todo task_by_id  1  
```  
positional arguments:  
-task_id 

####delete_task    
```  
todo delete_task 1
```   
positional arguments:    
-task_id   
####edit task parameters
 
```  
todo edit_task 6 title NEW
```   
positional arguments:   
-task_id   
-parameter_type  
-new_title

####get task_subtasks   
``` 
  todo get_subtasks 5
``` 
positional arguments:  
-task_id 
####share_permission  
``` 
todo share_permission  2 2
``` 
positional arguments:   
-new_user_id   
-task_id

####get task by tag
```
todo by_tag "example" 
``` 
positional arguments:   
-tag text
####tasks_on_period  
``` 
 todo tasks_on_period "31/12/12" "31/12/13" 
```  
positional arguments:  
-start_date   
-end_date

#Comments

####comment_task    
```  
todo comment_task 2 "comment text" 
```   
 
positional arguments:   
-task_id   
-text
#### get_comments   
```   
todo get_comments 2  
```  
positional arguments:  
-task_id 
#_________________

#User
#### get_comments 
```  
todo sign_up darya 123
```  
positional arguments:  
--login  
--password
#### get_comments 
```  
todo log_in darya 123
```  
positional arguments:  
--login  
--password

#### get_comments 
```  
todo log_out
```  
