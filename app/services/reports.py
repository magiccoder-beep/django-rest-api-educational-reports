from django.db.models import Count
from app.models.reports import Report
from rest_framework.pagination import PageNumberPagination

def get_reports_with_multiple_submissions(req, selected_agency, page_size):
    reports = (
        Report.objects.filter(agency=selected_agency)
        .annotate(submission_count=Count('submission'))
        .filter(submission_count__gt=1)
        .prefetch_related('submission_set')
        .order_by('id')
    )
    
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    paginated_reports = paginator.paginate_queryset(reports, req)
    
    response_data = [
        {
            "id": report.id,
            "name": report.name,
            "report": report.report,
            "domain": report.submission_count,
            "due_date": report.due_date,
            "submissions": [
                {
                    "id": submission.id,
                    "status": submission.status,
                }
                for submission in report.submission_set.all()
            ],
        }
        for report in paginated_reports
    ]

    # Prepare and return the paginated response
    return {
        "count": paginator.page.paginator.count,
        "next": paginator.get_next_link(),
        "previous": paginator.get_previous_link(),
        "results": response_data,
    }
