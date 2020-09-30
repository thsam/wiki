import markdown2
import os
import random
from django.shortcuts import render, redirect
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
    print("renderizando entrada")
    page=util.get_entry(entry) #entrega el md
    if page is not None: 
        print("renderizando a encyclopedia/entry.html ")
        return render(request,"encyclopedia/entry.html",{
            "entry":markdowner.convert(page),
            "entry_title":entry
            
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "entry_title": entry    
        })

def newEntry(request,edit="false"):
    if request.method =="POST": #cuando he llenado el form
        print("Post del nuevo formulario")
        form = NewEntryForm(request.POST) #declaramos una variable y traemos el requerimiento POST
        if form.is_valid(): #si es valido
            title=form.cleaned_data["title"] #obtengo los datos del formulario
            content=form.cleaned_data["content"]
            pagen=util.get_entry(title)
            print(edit)
            if (pagen is None or edit=="true"): #el titulo de la entrada es nuevo y no es edicion
                print("guardano el nuevo form")
                util.save_entry(title, f'# {title}\n\n{content}') #guardo la entrada y el contenido
                #page=util.get_entry(title)
                #return entry(request,title)
                print(title)
                return redirect(reverse("entry", args=(title,)))
                """ return render(request,"encyclopedia/entry.html", 
                {
                    "entry":markdowner.convert(page),
                    "entry_tile":title
             
                }) """
            else: #pagina existe
                print("No se puede guardar x la pagina existe")
                return render(request,"encyclopedia/new.html",
                {
                    "form": form, #le entrego la info, para que edite el titulo
                    "exist": True
                })
    else: #al principio muestro la plantilla con el formulario
        print("estoy creando un formulario")
        return render(request,"encyclopedia/new.html", {
            "form": NewEntryForm()
        }) 

def randomPage(request):
    entry_random=random.choice(util.list_entries())
    return entry(request,entry_random)
def edit(request,entry):
    print("entrando 1")
    if request.method =="GET": #1) doy el formulario para editar con la info
        page=util.get_entry(entry)
        #Para separar el titulo del contenido
        with open(f'./entries/{entry}.md') as ef:
            ef_content = ef.readlines()
        contenido=''.join(ef_content[1:])
        form = NewEntryForm(initial={'title':entry,'content':contenido})
        
        if page is not None: #2) la pagina existe
            return render(request,"encyclopedia/edit.html", {
                "form": form,
                "page_edit": entry
            })
        else: #3) no existe la pagina
            return render(request, "encyclopedia/error.html", {
            "entry_title": entry    
        })
    else:
        print("entrando true")
        return newEntry(request,"true")


        

           
            


