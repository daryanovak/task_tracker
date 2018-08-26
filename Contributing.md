#Commanline commands:

####NAME
####create_task 
"""
    creates a new single task  
"""

positional arguments:  
-title   
-text   
-status 

optional arguments:  
--tags   
--parent_title    
#___________________
####NAME
#### create_periodic_task 
"""  
creates a new periodic task   
"""  
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
#___________________
####NAME
#### get_tasks    
"""  
gets all user tasks  
"""
#___________________

####NAME
#### task_by_id    
"""  
gets task by id    
 """   
positional arguments:  
-task_id 
#___________________

####NAME
#### delete_task    
"""  
delete task by id   
 """  
positional arguments:    
-task_id 
#___________________
####NAME
#### edit_task_title    
"""  
edit task title by task id  
"""  
positional arguments:   
-task_id   
-new_title
#___________________
####NAME
####edit_task_text   
"""  
edit task text by title   
"""  
positional arguments:    
-task_id   
-new_text
#___________________
####NAME  
####edit_task_status   
 """  
 edit task status by title  
 """  
positional arguments:    
-task_id 
 -new_status
 #___________________
####NAME
####task_subtasks   
 """  
  gets subtasks of task by task_id  
 """
positional arguments:  
-task_id 
#___________________
####NAME
####share_permission   
"""  
share permission by user_id  
"""  
positional arguments:   
-user_id   
-task_title
#___________________
####NAME
####by_tag   
"""  
gets all task by tag  
"""  
positional arguments:   
-tag
#___________________
####NAME
####tasks_on_period  
 """  
 gets all task by date period  
 """  
positional arguments:  
-start_date   
-end_date
#___________________
#Comments

####NAME
####comment_task    
"""  
comment task by title   
"""  
positional arguments: 
-task_id   
-text
#___________________
####NAME
####get_comments   
"""  
gets task commnets by task_id  
"""  
positional arguments:  
-task_id 
#___________________
####NAME
####delete_comment   
"""  
deletes commnet by id  
"""  
positional arguments:  
-task_id 
#___________________