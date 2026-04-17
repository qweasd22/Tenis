from django import forms
from core.models import Partner
from documents.models import Category, Document
from eventcalendar.models import Event
class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ["name", "logo", "url"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "url": forms.URLInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["logo"].widget.attrs.update({"class": "form-control"})

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug", "order"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "order": forms.NumberInput(attrs={"class": "form-control"}),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["title", "description", "category", "file", "order"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "order": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["file"].widget.attrs.update({"class": "form-control"})

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "start_date",
            "end_date",
            "start_time",
            "end_time",
            "pdf",
            "is_current",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "start_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "end_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "is_current": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["pdf"].widget.attrs.update({"class": "form-control"})

from MediaPhoto.models import MediaEvent

class MediaEventForm(forms.ModelForm):
    class Meta:
        model = MediaEvent
        fields = ["title", "description", "date", "cover"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cover"].widget.attrs.update({"class": "form-control"})

from django.utils import timezone
from news.models import News

class NewsForm(forms.ModelForm):
    created_at = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(
            attrs={"class": "form-control", "type": "datetime-local"},
            format="%Y-%m-%dT%H:%M"
        ),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    class Meta:
        model = News
        fields = [
            "title",
            "slug",
            "full_description",
            "image",
            "created_at",
            "published",
            "show_in_slider",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "show_in_slider": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["image"].widget.attrs.update({"class": "form-control"})

        if self.instance and self.instance.pk and self.instance.created_at:
            self.initial["created_at"] = timezone.localtime(self.instance.created_at).strftime("%Y-%m-%dT%H:%M")
        elif not self.initial.get("created_at"):
            self.initial["created_at"] = timezone.localtime().strftime("%Y-%m-%dT%H:%M")

from projects.models import Project, ProjectCategory

class ProjectCategoryForm(forms.ModelForm):
    class Meta:
        model = ProjectCategory
        fields = ["title", "slug", "order", "is_active"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "order": forms.NumberInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "slug",
            "category",
            "short_description",
            "full_description",
            "main_image",
            "status",
            "start_date",
            "end_date",
            "location",
            "prize_fund",
            "contacts",
            "attachment",
            "external_link",
            "gallery_link",
            "order",
            "is_active",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "short_description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "prize_fund": forms.TextInput(attrs={"class": "form-control"}),
            "contacts": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "external_link": forms.URLInput(attrs={"class": "form-control"}),
            "gallery_link": forms.URLInput(attrs={"class": "form-control"}),
            "order": forms.NumberInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["main_image"].widget.attrs.update({"class": "form-control"})
        self.fields["attachment"].widget.attrs.update({"class": "form-control"})

from structure.models import Person
class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["full_name", "role", "photo", "is_active", "group"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "role": forms.TextInput(attrs={"class": "form-control"}),
            "group": forms.Select(attrs={"class": "form-select"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["photo"].widget.attrs.update({"class": "form-control"})

from teams.models import Season, TeamMember, Coach, Judge
class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ["year", "team_list_pdf"]
        widgets = {
            "year": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["team_list_pdf"].widget.attrs.update({"class": "form-control"})


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = [
            "full_name",
            "birth_date",
            "gender",
            "rank",
            "coach",
            "rating",
            "photo",
            "season",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "rank": forms.TextInput(attrs={"class": "form-control"}),
            "coach": forms.TextInput(attrs={"class": "form-control"}),
            "rating": forms.NumberInput(attrs={"class": "form-control"}),
            "season": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["photo"].widget.attrs.update({"class": "form-control"})


class CoachForm(forms.ModelForm):
    class Meta:
        model = Coach
        fields = ["full_name", "category", "photo"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["photo"].widget.attrs.update({"class": "form-control"})


class JudgeForm(forms.ModelForm):
    class Meta:
        model = Judge
        fields = ["full_name", "category", "photo"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["photo"].widget.attrs.update({"class": "form-control"})