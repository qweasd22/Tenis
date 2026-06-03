from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver

from core.models import Partner
from documents.models import Category, Document
from eventcalendar.models import Event
from MediaPhoto.models import MediaEvent
from news.models import News
from projects.models import Project, ProjectCategory
from qa.indexers import delete_index_for_instance, update_index_for_instance
from structure.models import Person
from teams.models import Coach, Judge, Season, TeamMember


@receiver(post_save, sender=News)
@receiver(post_save, sender=Project)
@receiver(post_save, sender=Category)
@receiver(post_save, sender=Document)
@receiver(post_save, sender=Event)
@receiver(post_save, sender=MediaEvent)
@receiver(post_save, sender=Person)
@receiver(post_save, sender=Partner)
@receiver(post_save, sender=TeamMember)
@receiver(post_save, sender=Season)
@receiver(post_save, sender=Coach)
@receiver(post_save, sender=Judge)
def refresh_qa_index_on_save(sender, instance, **kwargs):
    update_index_for_instance(instance)


@receiver(post_delete, sender=News)
@receiver(post_delete, sender=Project)
@receiver(post_delete, sender=Category)
@receiver(post_delete, sender=Document)
@receiver(post_delete, sender=Event)
@receiver(post_delete, sender=MediaEvent)
@receiver(post_delete, sender=Person)
@receiver(post_delete, sender=Partner)
@receiver(post_delete, sender=TeamMember)
@receiver(post_delete, sender=Season)
@receiver(post_delete, sender=Coach)
@receiver(post_delete, sender=Judge)
def delete_qa_index_on_delete(sender, instance, **kwargs):
    delete_index_for_instance(instance)


@receiver(post_save, sender=Category)
def refresh_documents_after_category_change(sender, instance, **kwargs):
    for document in instance.documents.select_related("category").prefetch_related("tags"):
        update_index_for_instance(document)


@receiver(post_save, sender=ProjectCategory)
def refresh_projects_after_category_change(sender, instance, **kwargs):
    for project in instance.projects.select_related("category"):
        update_index_for_instance(project)


@receiver(post_save, sender=Season)
def refresh_team_members_after_season_change(sender, instance, **kwargs):
    for member in instance.team_members.select_related("season"):
        update_index_for_instance(member)


@receiver(m2m_changed, sender=Document.tags.through)
def refresh_document_after_tags_change(sender, instance, action, **kwargs):
    if action in {"post_add", "post_remove", "post_clear"}:
        update_index_for_instance(instance)
