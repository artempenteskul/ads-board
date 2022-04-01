from .models import SubRubric


def add_rubrics_to_context_processor(request):
    context = {'rubrics': SubRubric.objects.all()}
    return context
