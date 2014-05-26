from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login

from manozodynas.forms import *
from manozodynas.models import *

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = LoginForm()
    #import ipdb; ipdb.set_trace()
    return render(request, 'manozodynas/login.html', {'form':form})


def word_view(request):
    # import pdb; pdb.set_trace()
    if request.method == 'POST':
        form_word = WordsForm(request.POST)
        if form_word.is_valid():
            form_word.save()
            form_word = WordsForm()
    else:
        form_word = WordsForm()

# wocabulary part
    word_info = Words.objects.order_by('key')    

# end of wocabulary part  
    return render(request, 'word.html', {
        'form_word':form_word,
        'USER': request.user,
        'wocabulary': word_info,
    })

def main_view(request, word_id):
    if request.method == 'POST':
        form = TranslationForm(request.POST) # construct form with errors
        form_word = WordsForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            form = TranslationForm()

        if form_word.is_valid():
            form_word.save()
            form_word = TranslationForm()

    else:
        form = TranslationForm()
        form_word = WordsForm()

# wocabulary part
    wocab = Translation.objects.order_by('key_word')    
    word_info = []
    if word_id >= 0:
        word  = Translation.objects.filter(id=word_id)
        arr = word[0].matches.split(" ")
        for elem in arr:
            curr = Words.objects.filter(key=elem)
            if len(curr) > 0:
                word_info.append(curr[0])
            else:
                word_info.append(Words(key=elem, description=""))
# end of wocabulary part  
    return render(request, 'main.html', {
        'form': form,
        'form_word':form_word,
        'USER': request.user,
        'wocabulary': wocab,
        'word_id': word_id,
        'word_info': word_info,
    })
