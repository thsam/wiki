import markdown2
from django.shortcuts import render

from . import util
from django.urls import reverse
from markdown2 import Markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,entry):
    markdowner= Markdown()
    page=util.get_entry(entry) #entrega el md
    if page is not None: 
        return render(request,"encyclopedia/entry.html",{
            "entry":markdowner.convert(page),
            "entry_title":entry
            
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "entry_title": entry    
        })



