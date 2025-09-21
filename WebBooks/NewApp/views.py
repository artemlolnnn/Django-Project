import requests
from django.shortcuts import *
from django.http import *
from .models import *
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import *
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import *
from datetime import datetime
from .forms import AuthorsForm
from django.core.mail import send_mail
from django.contrib import messages
from django.views.generic.edit import *
from django.urls import *

class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'NewApp/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user
        ).filter(
            status__exact='2'
        ).order_by('due_back')

class BookListView(generic.ListView):
    model = Book
    paginate_by = 3

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 4


def authors_add(request):
    author = Author.objects.all()
    authorsform = AuthorsForm()
    return render(request, 'NewApp/authors_add.html', context={'form': authorsform, 'author': author})

def create(request):
    if request.method == "POST":
        author = Author()
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get('last_name')
        author.date_of_birth = request.POST.get('date_of_birth')
        author.date_of_death = request.POST.get('date_of_death')
        author.save()
        return HttpResponseRedirect('/authors_add/')
    
def delete(request, id):
    try:
        author = Author.objects.get(id=id)
        author.delete()
        return HttpResponseRedirect('/authors_add/')
    except Author.DoesNotExist:
        return HttpResponseNotFound('<h2>Автор не найден</h2>')

def edit1(request, id):
    author = Author.objects.get(id=id)
    if request.method == "POST":
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get('last_name')
        author.date_of_birth = request.POST.get('date_of_birth')
        author.date_of_death = request.POST.get('date_of_death')
        author.save()
        return HttpResponseRedirect('/authors_add/')
    else:
        return render(request, "NewApp/edit1.html", context={"author": author})

# Create your views here.
def main(request):
    print(request.user)
    if request.user.username == "":
        request.session['logined'] = None

    if request.method == "POST":
        AuthorBookName = request.POST.get("AuthorOrBook")

        print(AuthorBookName)

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(request, 'Main.html', context={"books": len(Book.objects.all()), "authors": len(Author.objects.all()),'num_visits': num_visits+1})

def RD(request):
    return HttpResponseRedirect("/catalog/")

def checkEmpty(request):
    if request.POST.get('username') != "" and request.POST.get('password') != "": return True
    else: return False

def login(request):
    if request.method == "POST":
        if checkEmpty(request):
            if request.POST.get('sg') == 'login':
                try:
                    user = User.objects.get(username=request.POST.get('username'))
                    
                    if user.check_password(request.POST.get('password')):
                        messages.success(request, 'Вы успешно вошли в систему!')
                        request.session['logined'] = request.POST.get('username')
                        auth_login(request, user)
                        return HttpResponseRedirect('/')
                    else:
                        messages.error(request, 'Неверный пароль!')
                        
                except User.DoesNotExist:
                    messages.error(request, 'Пользователь с таким именем не найден!')
                    
            else:
                if request.POST.get('password') == request.POST.get('password2'):
                    username = request.POST.get('username')
                    if not User.objects.filter(username=username).exists():
                        try:
                            new_user = User()
                            new_user.email = request.POST.get('email')
                            new_user.username = username
                            new_user.set_password(request.POST.get('password'))
                            new_user.save()
                            messages.success(request, 'Регистрация прошла успешно! Добро пожаловать!')
                            auth_login(request, new_user)
                            request.session['logined'] = new_user.username
                        except Exception as e:
                            messages.error(request, f'Ошибка при сохранении пользователя: {e}')
                    else:
                        messages.error(request, 'Пользователь с таким именем уже существует!')
                else:
                    messages.error(request, 'Пароли не совпадают!')

    return render(request, 'NewApp/login.html')

'''def activate(request, email):
    activated = False
    for i in NotActivated:
        print(i) 
        if i[1] == email:
            i[0].save()
            request.session['logined'] = i[0].username
            auth_login(request, i[0])
            activated = True
    
    if not activated:
        return HttpResponse("Аккаунт не найден!")
    else:
        return HttpResponseRedirect('/')'''


    

@login_required
def logout(request):
    if request.method == "POST":
        request.session['logined'] = None
        auth_logout(request)
        return HttpResponseRedirect('/')

    return render(request, 'NewApp/logout.html')

@login_required
def reset_password(request):
    if request.method == "POST":
        return redirect('password_reset')

    return render(request, 'NewApp/reset_password.html')

@login_required
def book_booked(request, id):
    date_pick = request.POST.get('date_pick')

    book = get_object_or_404(BookInstance, pk=str(id))
    book.borrower = request.user
    book.status_id = 2
    book.save()


    return redirect('my-borrowed')