from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import SubRubric, Advert
from .forms import SearchForm, AdvertForm, AIFormSet


def index(request):
    ads = Advert.objects.filter(is_active=True)[:10]
    return render(request, 'index.html', {'ads': ads})


def by_rubric(request, pk):
    rubric = get_object_or_404(SubRubric, pk=pk)
    ads = Advert.objects.filter(is_active=True, rubric=pk)

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        ads = ads.filter(q)
    else:
        keyword = ''

    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(ads, 2)

    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1

    page = paginator.get_page(page_num)
    context = {'rubric': rubric, 'page': page, 'ads': page.object_list, 'form': form}
    return render(request, 'by_rubric.html', context)


def detail(request, rubric_pk, pk):
    ad = get_object_or_404(Advert, pk=pk)
    ad_images = ad.additionalimage_set.all()
    context = {'ad': ad, 'ad_images': ad_images}
    return render(request, 'detail.html', context)


@login_required
def add_new_ad(request):
    if request.method == 'POST':
        form = AdvertForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=ad)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, 'Advert was successfully added')
                return redirect('user:profile')
    else:
        form = AdvertForm(initial={'author': request.user.pk})
        formset = AIFormSet()
        return render(request, 'add_new_ad.html', {'form': form, 'formset': formset})
