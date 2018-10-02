from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.views.decorators.http import require_http_methods
from django.db import transaction

from .models import GifToUser, GifToUserCategory

HTTP_CREATED = 201
HTTP_ACCEPTED = 202
HTTP_NOT_FOUND = 404
HTTP_NOT_ALLOWED = 405


@login_required(login_url='/users/login/')
@require_http_methods(["GET", ])
def index(request):
    """
    The view for "See my Gifs"
    """
    cat_filter = request.GET.get('category_filter')
    context = {"cat_filter": cat_filter,
               "gifs_with_cats": GifToUser.get_user_gifs_for_category(
                   request.user, cat_filter=cat_filter),
               "all_cats": GifToUserCategory.get_user_categories(request.user)}
    template = loader.get_template('gifs/index.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/users/login/')
@require_http_methods(["GET", ])
def search(request):
    """
    The view for the "Search for New Gifs"
    """
    key = request.GET.get("key", "")
    context = {'gif_urls': []}
    if key:
        try:
            context = {'gif_urls': request.searchForNewGifs(key)}
        except LookupException as e:
            context['error'] = \
                'There was an error calling the API. Please try again.'
    template = loader.get_template('gifs/search.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/users/login/')
@require_http_methods(["POST", ])
@transaction.atomic
def new_gif(request, gif_url):
    """
    Endpoint used by javascript call to save new gifs
    """
    if GifToUser.objects.filter(gif_url=gif_url, user=request.user):
        # has already been saved
        return HttpResponse(status=HTTP_ACCEPTED)

    gtu = GifToUser(gif_url=gif_url, user=request.user)
    gtu.save()
    return HttpResponse(status=HTTP_CREATED)


@login_required(login_url='/users/login/')
@require_http_methods(["GET", ])
def gif_editor(request, gif_url):
    try:
        gtu = GifToUser.objects.get(gif_url=gif_url, user=request.user)
        template = loader.get_template('gifs/editor.html')
        gif_cats = []
        for gtc in GifToUserCategory.objects.filter(
                gif_to_user=gtu).order_by('category'):
            gif_cats.append(gtc.category)
        context = {'gtu': gtu,
                   'gif_cats': gif_cats,
                   'all_cats': GifToUserCategory.get_user_categories(
                       request.user)}
        return HttpResponse(template.render(context, request))
    except GifToUser.DoesNotExist:
        return HttpResponse(status=HTTP_NOT_FOUND)


@login_required(login_url='/users/login/')
@require_http_methods(["POST", ])
@transaction.atomic
def edit_gif_to_category(request, gif_url):
    """
    will remove current GifToUserCategory's if they are no longer valid
    """
    gtus = GifToUser.objects.filter(gif_url=gif_url, user=request.user)
    if not gtus:
        return HttpResponse(status=HTTP_NOT_FOUND)
    gtu = gtus[0]
    # remove categories not still there
    for gtc in GifToUserCategory.objects.filter(gif_to_user=gtu):
        if not request.POST.get(gtc.category):
            gtc.delete()
    return redirect('gifs:editor', gif_url=gif_url)


@login_required(login_url='/users/login/')
@require_http_methods(["POST", ])
@transaction.atomic
def add_gif_to_category(request, gif_url):
    gtus = GifToUser.objects.filter(gif_url=gif_url, user=request.user)
    if not gtus:
        return HttpResponse(status=HTTP_NOT_FOUND)
    gtu = gtus[0]
    new_cats = request.POST.getlist("newcategory", [])
    for cat in new_cats:
        if not cat:
            continue
        try:
            gtc = GifToUserCategory(category=cat, gif_to_user=gtu)
            gtc.save()
        except IntegrityError as e:
            pass
    return redirect('gifs:editor', gif_url=gif_url)


@login_required(login_url='/users/login/')
@require_http_methods(["POST", "DELETE"])
@transaction.atomic
def delete_gif_to_user(request, gif_url):
    gtus = GifToUser.objects.filter(gif_url=gif_url, user=request.user)
    if gtus:
        gtus[0].delete()
    else:
        return HttpResponse(status=HTTP_NOT_FOUND)
    return redirect('gifs:index')


def handler404(request, exception, template_name='404.html'):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler404(request, exception, template_name='404.html'):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response
