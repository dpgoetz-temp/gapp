from collections import OrderedDict
from django.db import models
from django.apps import apps
from django.contrib.auth.models import User
from django.conf import settings


class LookupException(Exception):
    pass


class GifToUser(models.Model):
    """
    This table holds the urls for the gifs the user has saved.
    If foreign keys into django's user table.
    """
    gif_url = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("gif_url", "user"),)

    @classmethod
    def get_user_gifs_for_category(cls, user, cat_filter=""):
        """
        search db for gifs for this user, optionally limited by cat_filter for
        gifs with category assigned.
        returns: list of tuples in form (gif_url, [category1, category2])
        """
        gifs_with_cats = []
        for gtu in GifToUser.objects.filter(user=user).order_by('create_date'):
            gtcs = []
            cat_match = not cat_filter  # if not sent all match
            for gtc in GifToUserCategory.objects.filter(gif_to_user=gtu):
                if cat_filter and cat_filter == gtc.category:
                    cat_match = True
                gtcs.append(gtc.category)
            if cat_match:
                gtcs.sort()
                gifs_with_cats.append((gtu.gif_url, gtcs))
        return gifs_with_cats


class GifToUserCategory(models.Model):
    """
    This table holfs the categories assigned to each gif the user has saved.
    It foreign keys to GifToUser and when a GifToUser is deleted the delete
    cascades to this table in SQL.
    """
    gif_to_user = models.ForeignKey(GifToUser, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)

    class Meta:
        unique_together = (("gif_to_user", "category"),)

    @classmethod
    def get_user_categories(cls, user):
        """
        search db for all categories this user has used on any gif
        returns: list of ordered category str's
        """
        all_cats = OrderedDict()
        for gtc in GifToUserCategory.objects.filter(
                gif_to_user__user=user).order_by('category'):
            all_cats[gtc.category] = True
        return all_cats.keys()
