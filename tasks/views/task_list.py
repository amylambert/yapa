from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, F, IntegerField, Value, When
from django.views import generic
from ..models import Task


class TaskListView(LoginRequiredMixin, generic.ListView):
    """Renders all user tasks sorted by project, deadline, and priority."""

    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        """Builds multi-tier sorting query execution chain."""
        # Map string choice priorities to logical numerical weights
        priority_weight = Case(
            When(priority="HIGH", then=Value(1)),
            When(priority="MEDIUM", then=Value(2)),
            When(priority="LOW", then=Value(3)),
            output_field=IntegerField(),
        )

        return (
            Task.objects.filter(owner=self.request.user)
            .annotate(p_weight=priority_weight)
            .order_by(
                F("project").asc(nulls_first=True),
                F("end_date").asc(nulls_last=True),
                "p_weight",
            )
        )