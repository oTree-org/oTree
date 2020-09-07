from django.shortcuts import render


def chat(request):
    return render(request, 'demo/chat.html')
