import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import TodoItem

@csrf_exempt
@require_http_methods(["GET", "POST"])
def todo_list(request):
    if request.method == 'GET':
        todos = TodoItem.objects.all()
        return JsonResponse([todo.to_dict() for todo in todos], safe=False)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        todo = TodoItem.objects.create(
            title=data.get('title', ''),
            description=data.get('description', ''),
            completed=data.get('completed', False)
        )
        return JsonResponse(todo.to_dict(), status=201)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def todo_detail(request, id):
    todo = get_object_or_404(TodoItem, id=id)
    
    if request.method == 'GET':
        return JsonResponse(todo.to_dict())
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        todo.title = data.get('title', todo.title)
        todo.description = data.get('description', todo.description)
        
        if 'completed' in data:
            todo.completed = bool(data['completed'])
            
        todo.save()
        return JsonResponse(todo.to_dict())
    
    elif request.method == 'DELETE':
        todo.delete()
        return HttpResponse(status=204)

@csrf_exempt
def gettodos_pox(request):
    if request.method == 'GET':
        todos = list(TodoItem.objects.values_list('title', flat=True))
        return JsonResponse(todos, safe=False)
    return HttpResponse(status=405)

@csrf_exempt
def getTodoById_pox(request):
    if request.method == 'GET':
        todo_id = request.GET.get('id')
        if todo_id:
            try:
                todo = TodoItem.objects.get(id=todo_id)
                return HttpResponse(f"Details of todo with ID: {todo_id}")
            except (TodoItem.DoesNotExist, ValueError):
                return HttpResponse(f"Todo with ID {todo_id} not found", status=404)
        return HttpResponse("No ID provided", status=400)
    return HttpResponse(status=405)

@csrf_exempt
def createTodo_pox(request):
    if request.method == 'POST':
        todo_text = request.GET.get('todo', '')
        if todo_text:
            todo = TodoItem.objects.create(title=todo_text)
            return HttpResponse(f"Created todo: {todo_text}")
        return HttpResponse("No todo provided", status=400)
    return HttpResponse(status=405)

@csrf_exempt
def test_hello(request):
    return JsonResponse({"message": "Hello"}, safe=False)