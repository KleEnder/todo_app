#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Task

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("main.html")

class EnterTaskHandler(BaseHandler):
    def post(self):
        name = self.request.get("task_name")
        message = self.request.get("task_message")
        message2 = self.request.get("task_message2")
        checked = bool(self.request.get("task_check"))

        task = Task(name=name, message=message, message2=message2, checked=checked)
        task.put()

        return self.write("You have written: " + "\n" + " name: " + name + " message: " + message + " message2: " +
                          message2 + " check: " + str(checked))

class AllTasksHandler(BaseHandler):
    def get(self):
        tasks = Task.query(Task.deleted == False).fetch()
        params = {'tasks': tasks}
        return self.render_template("all_tasks.html", params=params)

class AllTrueTasksHandler(BaseHandler):
    def get(self):
        tasks = Task.query(Task.deleted == True).fetch();
        params = {'tasks': tasks}
        return self.render_template("all_tasks_t.html", params=params)

class SingleTaskHandler(BaseHandler):
    def get(self, task_id):
        task = Task.get_by_id(int(task_id))
        params = {"task": task}
        return self.render_template("single_task.html", params=params)

class SingleTrueTaskHandler(BaseHandler):
    def get(self, task_id):
        task = Task.get_by_id(int(task_id))
        params = {"task": task}
        return self.render_template("single_true_task.html", params=params)

class EditTaskHandler(BaseHandler):
    def get(self, task_id):
        task = Task.get_by_id(int(task_id))
        params = {"task": task}
        return self.render_template("edit_task.html", params=params)

    def post(self, task_id):
        name = self.request.get("task_name")
        message = self.request.get("task_message")
        message2 = self.request.get("task_message2")
        checked = bool(self.request.get("task_check"))
        task = Task.get_by_id(int(task_id))
        task.name = name
        task.message = message
        task.message2 = message2
        task.checked = checked
        task.put()
        return self.redirect_to("all-tasks")

class EditTrueTaskHandler(BaseHandler):
    def get(self, task_id):
        task = Task.get_by_id(int(task_id))
        params = {"task": task}
        return self.render_template("edit_task_t.html", params=params)

    def post(self, task_id):
        name = self.request.get("task_name_t")
        message = self.request.get("task_message_t")
        message2 = self.request.get("task_message2_t")
        checked = bool(self.request.get("task_check_t"))
        deleted = not(bool(self.request.get("task_delete_t")))
        task = Task.get_by_id(int(task_id))
        task.name = name
        task.message = message
        task.message2 = message2
        task.checked = checked
        task.deleted = deleted
        task.put()
        return self.redirect_to("all-tasks-t")

class DeleteTaskHandler(BaseHandler):
    def get(self, task_id):
        task = Task.get_by_id(int(task_id))
        params = {"task": task}
        return self.render_template("delete_task.html", params=params)

    def post(self, task_id):
        task = Task.get_by_id(int(task_id))
        task.deleted = True
        task.put()
        return self.redirect_to("all-tasks")

class DeleteFinallyTaskHandler(BaseHandler):
    def get(self, task_id):
        task = Task.get_by_id(int(task_id))
        params = {"task": task}
        return self.render_template("delete_task_t.html", params=params)

    def post(self, task_id):
        task = Task.get_by_id(int(task_id))
        task.key.delete()
        return self.redirect_to("all-tasks-t")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/tasks', EnterTaskHandler),
    webapp2.Route('/all-tasks', AllTasksHandler, name="all-tasks"),
    webapp2.Route('/all-tasks-t', AllTrueTasksHandler, name="all-tasks-t"),
    webapp2.Route('/single-task/<task_id:\\d+>', SingleTaskHandler),
    webapp2.Route('/single-task-t/<task_id:\\d+>', SingleTrueTaskHandler),
    webapp2.Route('/single-task/<task_id:\\d+>/edit', EditTaskHandler),
    webapp2.Route('/single-task-t/<task_id:\\d+>/edit-finally', EditTrueTaskHandler),
    webapp2.Route('/single-task/<task_id:\\d+>/delete', DeleteTaskHandler),
    webapp2.Route('/single-task-t/<task_id:\\d+>/delete-finally', DeleteFinallyTaskHandler),
], debug=True)

