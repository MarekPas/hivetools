from django.shortcuts import render
import hashlib

def encode_answer(request):
    if request.method == "POST":
        salted_password = request.POST.get('username').strip().lower() + request.POST.get('answer').strip().lower()
        hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
        return render(request, 'answers/answers.html', {'hashed_password': hashed_password})
    else:
        return render(request, 'answers/answers.html')


