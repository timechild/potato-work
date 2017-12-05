from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel

from djangae.fields import RelatedSetField


class Project(TimeStampedModel):
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    def __str__(self):
        return self.title

    def get_project_by_ticket(self, ticket_id):
        return Ticket.objects.filter(pk=int(ticket_id)).first().project

    def get_ordered_project_list(self, user_id):

        all_projects = Project.objects.all()
        user_projects = [user_tickets.project for user_tickets in Ticket.objects.filter(assignees=user_id)]

        oredered_list = []
        for project in all_projects:
            if project in user_projects:
                oredered_list.insert(0, project)
            else:
                oredered_list.append(project)

        return oredered_list


class Ticket(TimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, related_name="tickets")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name="created_tickets")
    assignees = RelatedSetField(
        settings.AUTH_USER_MODEL, related_name="tickets")

    def __str__(self):
        return self.title

    def delete_ticket(self, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.delete()
