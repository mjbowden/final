from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from .models import *
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
# Create your views here.
class Home(TemplateView):
    template_name = "home.html"
class ReviewCreateView(CreateView):
  model = Review
  template_name = "review/review_form.html"
  fields = ['title', 'description']
  success_url = reverse_lazy('review_list')

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super (ReviewCreateView, self).form_valid(form)
class ReviewListView(ListView):
    model = Review
    template_name = "review/review_list.html"
class ReviewDetailView(DetailView):
    model = Review
    template_name = 'review/review_detail.html'
class ReviewUpdateView(UpdateView):
    model = Review
    template_name = 'review/review_form.html'
    fields = ['title', 'review']
class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'review/review_confirm_delete.html'
    sucess_url = reverse_lazy('review_list')
class ReplyCreateView(CreateView):
    model = Reply
    template_name = "reply/reply_form.html"
    fields = ['text']
    
    def get_success_url(self):
      return self.object.review.get_absolute_url()

    def form_valid(self, form):
      form.instance.user = self.request.user
      form.instance.review = Review.objects.get(id=self.kwargs['pk'])
      return super (ReplyCreateView, self).form_valid(form)