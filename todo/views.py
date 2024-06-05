from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View, generic
from django.contrib.auth import authenticate, login

from todo.forms import *
from todo.models import *


class Index(View):
    template_name = 'todo/index.html'

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        tasks_completed = Task.objects.filter(completed=True)
        tasks_not_completed = Task.objects.exclude(completed=True)

        return render(request, self.template_name,
                      {'tasks': tasks, 'tasks_completed': tasks_completed, 'tasks_not_completed': tasks_not_completed})


class RegisterView(generic.View):
    template_name = 'todo/auth/register.html'
    login_template = 'todo/auth/login.html'
    form = RegisterForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password == confirm_password:
                user = CustomUser.objects.create_user(
                    email=email,
                    password=password
                )
                user.username = username
                user.save()
                return render(request, self.login_template,
                              {'form': form, 'success': 'You have registered successfully'})

            return render(request, self.template_name,
                          {'form': form, 'confirmed_password': 'Your password and confirm password must be the same'})
        return render(request, self.template_name, {'form': form})


class LoginView(generic.View):
    template_name = 'todo/auth/login.html'
    form = LoginForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('todo:index'))
            else:
                return render(request, self.template_name,
                              {"error": "Your email or password is not valid", 'form': form})

        return render(request, self.template_name, {'form': form})


class CreateTask(generic.View):
    template_name_if_form_valid = "todo/partials/tasks.html"
    template_name_if_not_form_valid = ""
    form = TaskForm

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)

        tasks = Task.objects.all()
        tasks_completed = Task.objects.filter(completed=True)
        tasks_not_completed = Task.objects.exclude(completed=True)

        if form.is_valid():
            title = form.cleaned_data['title']
            user = request.user

            task = Task.objects.create(title=title, owner=user)

            return render(request, self.template_name_if_form_valid,
                          {'task': task, 'tasks': tasks, 'tasks_completed': tasks_completed,
                           'tasks_not_completed': tasks_not_completed})

        return render(request, self.template_name_if_not_form_valid, {'form': self.form})


class CompletedTask(generic.View):
    template_name = 'todo/partials/tasks.html'

    def post(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        tasks = Task.objects.all()
        tasks_completed = Task.objects.filter(completed=True)
        tasks_not_completed = Task.objects.exclude(completed=True)

        if task:
            task.completed = True if not task.completed else False
            task.save()

        return render(request, self.template_name, {'task': task, 'tasks': tasks, 'tasks_completed': tasks_completed,
                                                    'tasks_not_completed': tasks_not_completed})


class EditTask(generic.View):
    template_name = 'todo/partials/task.html'
    template_name_form = 'todo/partials/task_form.html'
    form = TaskForm

    def get(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        return render(request, self.template_name_form, {'task': task})

    def post(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        data = {
            'title': task.title
        }
        form = self.form(request.POST, initial=data)

        if form.is_valid():
            if form.has_changed():
                task.title = form.cleaned_data['title']
                task.save()

            return render(request, self.template_name, {'task': task})

        return render(request, self.template_name, {'task': task})


class GetTask(generic.View):
    template_name = 'todo/partials/task.html'

    def get(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        return render(request, self.template_name, {'task': task})


class DeleteTask(generic.View):
    template_name = 'todo/partials/tasks.html'

    def post(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        tasks = Task.objects.all()
        tasks_completed = Task.objects.filter(completed=True)
        tasks_not_completed = Task.objects.exclude(completed=True)
        if task:
            task.delete()

            return render(request, self.template_name, {'tasks': tasks, 'tasks_completed': tasks_completed,
                                                        'tasks_not_completed': tasks_not_completed})


class SearchTask(generic.View):
    template_name = 'todo/partials/tasks.html'

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.filter(title__contains=request.GET['search'])

        return render(request, self.template_name, {'tasks': tasks})
