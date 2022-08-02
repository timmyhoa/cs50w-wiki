from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

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

def search(request):
    query = request.GET['q'].strip().lower()
    allEntries = util.list_entries()
    possibleResult = []
    for entry in allEntries:
        if entry.lower() == query:
            return HttpResponseRedirect(reverse('entry', args=[entry]))
        if query in entry:
            possibleResult.append(entry)
    return render(request, "encyclopedia/search.html", {
        "entries": possibleResult,
    })
        
    # return render(request, "encyclopedia/search.html")
