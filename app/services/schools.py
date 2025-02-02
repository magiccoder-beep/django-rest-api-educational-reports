from django.db.models import Count
from app.models.schools import School
from rest_framework.pagination import PageNumberPagination

def get_schools_with_multiple_submissions(req, selected_agency, page_size):
    """
    Fetch paginated list of schools with more than 1 submission for a given agency.
    
    Args:
        selected_agency (str): The agency to filter schools by.
        page_size (int): The number of items per page.
    
    Returns:
        dict: A dictionary containing paginated school data and pagination metadata.
    """
    # Filter and annotate schools with submission counts
    schools = (
        School.objects.filter(agency=selected_agency)
        .annotate(submission_count=Count('submission'))
        .filter(submission_count__gt=1)
        .prefetch_related('submission_set')
        .order_by('id')
    )
    
    # Initialize pagination
    paginator = PageNumberPagination()
    paginator.page_size = page_size

    # Paginate the filtered schools
    paginated_schools = paginator.paginate_queryset(schools, req)

    # Serialize the paginated schools
    response_data = [
        {
            "id": school.id,
            "name": school.name,
            "gradeserved": school.gradeserved,
            "submissions": [
                {
                    "id": submission.id,
                    "status": submission.status,
                }
                for submission in school.submission_set.all()
            ],
        }
        for school in paginated_schools
    ]

    # Prepare and return the paginated response
    return {
        "count": paginator.page.paginator.count,
        "next": paginator.get_next_link(),
        "previous": paginator.get_previous_link(),
        "results": response_data,
    }
