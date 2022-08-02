from ast import arg
from cProfile import label
from importlib.machinery import WindowsRegistryFinder
from attr import attr
from django.shortcuts import render
from django.http import Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from django import forms

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

class newPageForm(forms.Form):
    entryTitle = forms.CharField(label='Page Title')
    content = forms.CharField(label='Content', widget=forms.Textarea())


def newPage(request):
    if request.method == 'GET':
        form = newPageForm()
        return render(request, "encyclopedia/newPage.html", {
            'form': form,
        })
    
    form = newPageForm(request.POST)
    if form.is_valid():
        form = form.cleaned_data
        entryTitle, content = form['entryTitle'], form['content']
        allEntries = util.list_entries()
        if entryTitle in allEntries:
            return HttpResponseBadRequest("Entry already exists")
        with open(f'./entries/{entryTitle}.md', 'w') as f:
            print(f'# {entryTitle}', file=f)
            print(f'{content}', file=f)
        return HttpResponseRedirect(reverse('entry', args=[entryTitle]))



    