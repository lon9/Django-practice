# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, get_object_or_404,\
    redirect
from django.http import HttpResponse
from django.template.context import RequestContext
from cms.forms import BookForm, ImpressionForm
from cms.models import Book, Impression
from django.views.generic.list import ListView
from django.db.transaction import commit

# Create your views here.
def book_list(request):
    '''書籍の一覧'''
    books = Book.objects.all().order_by('id')
    return render_to_response('cms/book_list.html',  #使用するテンプレート
                              {'books': books},      #テンプレ^とに渡すデータ
                              context_instance=RequestContext(request))  #その他の標準のコンテキスト

def book_edit(request, book_id=None):
    '''書籍の編集'''
    #return HttpResponse(u'書籍の編集')
    if book_id:
        book = get_object_or_404(Book, pk=book_id)
    else:
        book = Book()
        
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book) #POSTされたrequestデータからフォームを作成
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            return redirect('cms:book_list')
    else:
        form = BookForm(instance=book)  #bookインスタンスからフォームを作成
            
    return render_to_response('cms/book_edit.html',
                                  dict(form=form, book_id=book_id),
                                  context_instance=RequestContext(request))

def book_del(request, book_id):
    '''書籍の削除'''
#     return HttpResponse(u'書籍の削除')
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    return redirect('cms:book_list')

class ImpressionList(ListView):
    '''感想の一覧'''
    content_object_name='impressions'
    template_name='cms/impression_list.html'
    paginate_by=2
    
    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs['book_id'])
        impressions = book.impressions.all().order_by('id')
        self.object_list=impressions
        
        context = self.get_context_data(object_list=self.object_list, book=book)
        return self.render_to_response(context)
    
def impression_edit(request, book_id, impression_id=None):
    '''感想の編集'''
    book = get_object_or_404(Book, pk=book_id)
    if impression_id:
        impression = get_object_or_404(Impression, pk=impression_id)
    else:
        impression = Impression()
    
    if request.method=='POST':
        form = ImpressionForm(request.POST, instance=impression)
        if form.is_valid():
            impression = form.save(commit=False)
            impression.book = book
            impression.save()
            return redirect('cms:impression_list', book_id=book_id)
    else:
        form = ImpressionForm(instance=impression)
        
    return render_to_response('cms/impression_edit.html',
                              dict(form=form, book_id=book_id, impression_id= impression_id),
                              context_instance=RequestContext(request))

def impression_del(request, book_id, impression_id):
    '''感想の削除'''
    impression = get_object_or_404(Impression, pk=impression_id)
    impression.delete()
    return redirect('cms:impression_list', book_id=book_id)
