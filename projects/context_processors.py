from django.db.models import F
from .models import Project


def active_projects_processor(request):
    """Injects user-specific projects sorted by impending deadline safely."""
    if request.user.is_authenticated:
        # Sorting placeholder logic: Projects with deadlines first, ascending order
        projects = Project.objects.filter(owner=request.user).order_by(
            F("end_date").asc(nulls_last=True), 
            "-created_at"
        )
        return {"sidebar_projects": projects}
    return {"sidebar_projects": []}