from django.shortcuts import render
from django.http import Http404

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    data = util.get_entry(entry)
    data = util.convertMdHtml(data)
    if data is None:
        raise Http404("The entry does not exists")
    return render(request, 'encyclopedia/entry.html', {
        'title': entry,
        'data': data,
    })



