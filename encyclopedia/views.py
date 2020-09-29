import markdown2
from django.shortcuts import render
from django import forms
from . import util
from django.urls import reverse
from markdown2 import Markdown
from django.http import HttpResponse

markdowner= Markdown()
class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows' : 10}))
    #edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,entry):
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

def newEntry(request):
    if request.method =="POST": #cuando he llenado el form
        form = NewEntryForm(request.POST) #declaramos una variable y traemos el requerimiento POST
        if form.is_valid(): #si es valido
            title=form.cleaned_data["title"] #obtengo los datos del formulario
            content=form.cleaned_data["content"]
            pagen=util.list_entries()
            if title in pagen: #el titulo de la entrada es nuevo
                util.save_entry(title,content) #guardo la entrada y el contenido
                page=util.get_entry(title)
                return render(request,"encyclopedia/new.html", 
                {
                    "entry":markdowner.convert(page),
                    "entry_tile":title
             
                })
            else: #pagina existe
                return HttpResponse("<h1 style=\"color:blue\">Existe</h1>")
    else: #al principio muestro la plantilla con el formulario
        return render(request,"encyclopedia/new.html", {
            "form": NewEntryForm()
        }) 
            
            


