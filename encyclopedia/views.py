from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from random import randint
from random import choice
import random
import markdown2
from markdown2 import Markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "entrynumber": len(util.list_entries()),
    })


def findentry(request, name):
    markdowner = Markdown()
    content = util.get_entry(name)
    # markdowner.convert(content)
    return render(request, "encyclopedia/findentry.html", {
        "entries": markdowner.convert(content),
        "title": name,
        "noentry": util.get_entry(name) == None
    })


def search(request):
    originallist = util.list_entries()  # 原本的list
    search = []  # 有找到list的放入
    usersearch = str(request.GET['q'])
    if util.get_entry(usersearch) != None:
        return render(request, "encyclopedia/findentry.html", {
            "entries": util.get_entry(usersearch),
            "title": usersearch,
            "noentry": util.get_entry(usersearch) == None
        })
    else:
        for i in range(len(originallist)):
            a = originallist[i].find(usersearch)
            if (a != -1):
                search.append(originallist[i])
        return render(request, "encyclopedia/search.html", {
            "searchlist": search,
            "number": len(search)
        })


class NewEntryForm(forms.Form):
    entryname = forms.CharField(label='')
    entrydata = forms.CharField(widget=forms.Textarea(), label='')


def addnewpage(request):
    if request.method == "POST":
        entryinfo = NewEntryForm(request.POST)
        if entryinfo.is_valid():
            thename = entryinfo.cleaned_data["entryname"]
            thedata = entryinfo.cleaned_data["entrydata"]
            havelist = util.get_entry(thename)
            if havelist != None:
                return render(request, "encyclopedia/findentry.html", {
                    "noen": "Page already exist"
                })
            else:
                util.save_entry(thename, thedata)
                return render(request, "encyclopedia/findentry.html", {
                    "entries": util.get_entry(thename),
                    "title": thename
                })
    else:
        return render(request, "encyclopedia/addnewpage.html", {
            "entryinfo": NewEntryForm
        })


class EditEntryForm(forms.Form):
    EDITdata = forms.CharField(widget=forms.Textarea(), label='')


def edit(request, titlename):
    originalcontent = util.get_entry(titlename)
    if request.method == "POST":
        editinfo = EditEntryForm(request.POST)
        if editinfo.is_valid():
            updateddata = editinfo.cleaned_data["EDITdata"]
            util.save_entry(titlename, updateddata)
            return render(request, "encyclopedia/findentry.html", {
                "entries": util.get_entry(titlename),
                "title": titlename
            })
    else:
        return render(request, "encyclopedia/edit.html", {
            "entries": EditEntryForm({"EDITdata": originalcontent}),
            "title": titlename
        })


def theone(request):
    test = util.list_entries()
    randomchoice = str(random.choice(test))
    return HttpResponseRedirect(reverse('findentry', args=[randomchoice]))
