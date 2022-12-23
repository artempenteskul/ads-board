from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import SubRubric, Advert, Comment
from .forms import SearchForm, AdvertForm, AIFormSet, UserCommentForm, GuestCommentForm


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
    comments = Comment.objects.filter(advert=pk, is_active=True)

    initial = {'advert': ad.pk}
    if request.user.is_authenticated:
        initial['author'] = request.user.username
        form_class = UserCommentForm
    else:
        form_class = GuestCommentForm

    form = form_class(initial=initial)

    if request.method == 'POST':
        c_form = form_class(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.add_message(request, messages.SUCCESS, 'Comment was added')
        else:
            form = c_form
            messages.add_message(request, messages.WARNING, 'Comment was not added')

    context = {'ad': ad, 'ad_images': ad_images, 'comments': comments, 'form': form}
    return render(request, 'detail.html', context)


@login_required
def add_ad(request):
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
        return render(request, 'add_ad.html', {'form': form, 'formset': formset})


@login_required
def change_ad(request, pk):
    ad = get_object_or_404(Advert, pk=pk)
    if request.method == 'POST':
        form = AdvertForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            ad = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=ad)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, 'Advert was successfully changed')
                return redirect('user:profile')
    else:
        form = AdvertForm(instance=ad)
        formset = AIFormSet(instance=ad)
        return render(request, 'change_ad.html', {'form': form, 'formset': formset})


@login_required
def delete_ad(request, pk):
    ad = get_object_or_404(Advert, pk=pk)
    if request.method == 'POST':
        ad.delete()
        messages.add_message(request, messages.SUCCESS, 'Advert was deleted')
        return redirect('user:profile')
    else:
        return render(request, 'delete_ad.html', {'ad': ad})
