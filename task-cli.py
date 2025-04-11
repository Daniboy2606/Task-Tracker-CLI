import argparse
import json
import os
from datetime import datetime

#Variables globales
TASKS_FILE = 'tasks.json'

def add_task(description):
    '''Añande una nueva tarea'''
    tasks = load_tasks()
    new_id = max([task['id'] for task in tasks], default = 0) + 1
    
    #Obtener la hora actual en formato ISO
    current_time = datetime.now().isoformat()
    
    #Crear la nueva tarea
    new_task = {
        'id': new_id,
        'description': description,
        'status': 'todo',
        'created_at': current_time,
        'updatedAt': current_time
    }
    
    #Añadir la tarea a la lista
    tasks.append(new_task)
    
    #Guardar la lista actualizada
    save_tasks(tasks)
    
    return new_id
    
    
def update_task(task_id, description):
    tasks = load_tasks()
    
    #Buscar la tarea por id
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = description
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)  
            return True
    return False
    

def delete_task(task_id):
    tasks = load_tasks()
    
    # Creamos una nueva lista filtrando el task a eliminar
    updated_tasks = [task for task in tasks if task['id'] != task_id]
    
    # Verificamos si se eliminó alguna tarea
    if len(tasks) != len(updated_tasks):
        # Guardamos la lista actualizada
        save_tasks(updated_tasks)  
        return True
    return False
         

def mark_task(task_id, status):
    """Marca una tarea en un estado especifico"""
    if status not in ['todo', 'in-progress', 'done']:
        return False
    
    tasks = load_tasks()
    
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            return True
    return False

def list_tasks(status = None):
    """Lista las tareas filtradas por estado si es necesario"""
    tasks = load_tasks()
    
    if status:
        tasks = [task for task in tasks if task['status'] == status]
        return tasks
    else:
        #Si no hay estado, retornamos todas las tareas
        return tasks

#Funciones para manejar el archivo JSON
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []
        
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        return json.dump(tasks, file, indent=2)

#Funcion principal
def main():
    parser = argparse.ArgumentParser(description = 'Task Tracker CLI')
    subparser = parser.add_subparsers(dest='command', help = 'Command to execute')
    
    #Comando add
    add_parser = subparser.add_parser('add', help = 'Add a new task')
    add_parser.add_argument('description', help = 'Task description')
    
    #Comando update
    update_parser = subparser.add_parser('update', help = 'Update a task')
    update_parser.add_argument('id', type = int, help = 'Task ID')
    update_parser.add_argument('description', help = 'New task description')
    
    #Comando delete
    delete_parser = subparser.add_parser('delete', help = 'Delete a task')
    delete_parser.add_argument('id', type = int, help = 'Task ID')
    
    #Comando mark-in-progress
    in_progress_parser = subparser.add_parser('mark-in-progress', help = 'Mark a task as in-progress')
    in_progress_parser.add_argument('id', type = int, help = 'Task ID')
    
    #Comando mark-done
    done_parser = subparser.add_parser('mark-done', help = 'Mark a task as done')
    done_parser.add_argument('id', type = int, help = 'Task ID')
    
    #Comando list
    list_parser = subparser.add_parser('list', help = 'List all tasks')
    list_parser.add_argument('status',  nargs = '?',choices = ['todo', 'in-progress', 'done'], help = 'Filter tasks by status')
    
    try:
    
        args = parser.parse_args()
        if not args.command:
            parser.print_help()
            return
        
        #Manejar los comandos
        
        if args.command == 'add':
            task_id = add_task(args.description)
            print(f'Task added succesfully (ID: {task_id})')
        elif args.command == 'update':
            if update_task(args.id, args.description):
                print(f'Task {args.id} updated successfully')
            else:
                print(f'Task {args.id} not found')
        elif args.command == 'delete':
            if delete_task(args.id):
                print(f'Task {args.id} deleted successfully')
            else:
                print(f'Task {args.id} not found')
        elif args.command == 'mark-in-progress':
            if mark_task(args.id, 'in-progress'):
                print(f'Task {args.id} marked as in-progress')
            else:
                print(f'Task {args.id} not found')
        elif args.command == 'mark-done':
            if mark_task(args.id, 'done'):
                print(f'Task {args.id} marked as done')
            else:
                print(f'Task {args.id} not found')
        elif args.command == 'list':
            tasks = list_tasks(args.status)
            if not tasks:
                print('No tasks found')
            else:
                print(f"{'ID':<5}{'STATUS':<12}{'DESCRIPTION':<50}")
                print("-" * 67)
                for task in tasks:
                    print(f'{task["id"]:<5}{task["status"]:<12}{task["description"]:<50}')
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1         

if __name__ == '__main__':
    main()
