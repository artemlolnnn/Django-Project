"""
URL configuration for WebBooks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from NewApp import views
from django.urls import re_path as url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.RD, name="index"),
    path('catalog/', views.main),
    #path('catalog/books/', views.BooksCatalog, name="CatalogBooks"),
    #path('catalog/authors/', views.AuthorsCatalog, name="CatalogAuthors"),
    path('admin/', admin.site.urls),
    url(r'^books/$', views.BookListView.as_view(), name='books'),
    url(r'^books/(?P<pk>\d+)$', views.BookDetailView.as_view(), name="book-detail"),
    url(r'^authors/$', views.AuthorListView.as_view(), name="authors"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('reset/', views.reset_password, name='reset'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name="my-borrowed"),
    path('book_booked/<int:id>/', views.book_booked, name="book-booked"),
    path('authors_add/', views.authors_add, name='authors_add'),
    path('edit1/<int:id>/', views.edit1, name='edit1'),
    path('create/', views.create, name='create'),
    path('delete/<int:id>/', views.delete, name='delete'),
    url(r'^book/create/$', views.BookCreate.as_view(), name="book_create"),
    url(r'^book/update/(?P<pk>\d+)$', views.BookUpdate.as_view(), name="book_update"),
    url(r'^book/delete/(?P<pk>\d+)$', views.BookDelete.as_view(), name="book_delete")
    #path('ActivateEmail/<str:email>', views.activate, name="ActivateEmail")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
