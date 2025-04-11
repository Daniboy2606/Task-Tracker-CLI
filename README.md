# Task Tracker CLI 
Sample solution in python for the task-tracker challenge from roadmap.sh.

## How to run

Clone the repository and run the following command:

```bash
git clone https://github.com/Daniboy2606/Task-Tracker-CLI.git
cd Task-Tracker-CLI
```
```bash

# To add a task
python task-cli.py add "Buy groceries"

# To update a task
python task-cli.py update 1 "Buy groceries and cook dinner"

# To delete a task
python task-cli.py delete 1

# To mark a task as in progress/done
python task-cli.py mark-in-progress 1
python task-cli.py mark-done 1

# To list all tasks
python task-cli.py list
python task-cli.py list done
python task-cli.py list todo
python task-cli.py list in-progress
```

