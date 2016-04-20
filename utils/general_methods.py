import json
import urllib
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse


def get_json_response(python_dict):
    json_string = json.dumps(python_dict, cls=DjangoJSONEncoder)
    return HttpResponse(json_string, content_type='application/json')

def build_url(*args, **kwargs):
    get = kwargs.pop('get', {})
    url = reverse(*args, **kwargs)
    if get:
        url += '?' + urllib.urlencode(get)
    return url