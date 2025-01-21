from django.contrib.auth.decorators import login_required
from .models import query

@login_required
def query_count(request):
    if request.user.is_authenticated and request.user.is_staff:
      
        unresolved_queries = query.objects.filter(status="Pending").count()
        return {
            
            'unresolved_queries': unresolved_queries,
        }
    return {}
