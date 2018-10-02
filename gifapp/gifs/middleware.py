import os
import sys
from functools import partial
from django.conf import settings
import giphy_client
from giphy_client.rest import ApiException
from .models import LookupException


def giphy_seacher(giphyClient, giphy_api_key, search_key):
    """
    returns: list of string gif urls matching the key sent in
    raises: LookupException if error with api call
    """
    try:
        resp = giphyClient.gifs_search_get(
            giphy_api_key, search_key, **settings.GIPHY_KWARGS)
    except (ApiException, KeyError):
        raise LookupException(ApiException)
    try:
        return [d.images.fixed_width.url for d in resp.data]
    except AttributeError:
        raise LookupException("invalid data")


class GiphyClientMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.giphy_client = giphy_client.DefaultApi()
        if "GIPHY_API_KEY" in os.environ:
            self.giphy_api_key = os.environ["GIPHY_API_KEY"]
        else:
            print(
                "!! ERROR Please provide GIPHY_API_KEY environ var ERROR !!")
            sys.exit(1)

    def __call__(self, request):
        request.searchForNewGifs = partial(
            giphy_seacher, self.giphy_client, self.giphy_api_key)
        return self.get_response(request)
