from .models import SubRubric


def ads_board_context_processor(request):
    context = dict()
    context['rubrics'] = SubRubric.objects.all()
    return context
