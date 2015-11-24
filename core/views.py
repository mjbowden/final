from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from .models import *
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.core.exceptions import PermissionDenied
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
    def get_context_data(self, **kwargs):
        context = super(ReviewDetailView, self).get_context_data(**kwargs)
        review = Review.objects.get(id=self.kwargs['pk'])
        replies = Reply.objects.filter(review=review)
        context['replies'] = replies
        user_replies = Reply.objects.filter(review=review, user=self.request.user)
        context['user_replies'] = user_replies
        return context
class ReviewUpdateView(UpdateView):
    model = Review
    template_name = 'review/review_form.html'
    fields = ['title', 'review']
    def get_object(self, *args, **kwargs):
        object = super(ReviewUpdateView, self).get_object(*args, **kwargs)
        if object.user != self.request.user:
          raise PermissionDenied()
          return object
class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'review/review_confirm_delete.html'
    sucess_url = reverse_lazy('review_list')
    def get_object(self, *args, **kwargs):
        object = super(ReviewDeleteView, self).get_object(*args, **kwargs)
        if object.user !=self.request.user:
            raise PermissionDenied()
        return object
class ReplyCreateView(CreateView):
    model = Reply
    template_name = "reply/reply_form.html"
    fields = ['text']

    def get_success_url(self):
      return self.object.review.get_absolute_url()

    def form_valid(self, form):
      review = Review.objects.get(id=self.kwargs['pk'])
      if Reply.objects.filter(review=review, user=self.request.user).exists():
          raise PermissionDenied()
      form.instance.user = self.request.user
      form.instance.review = Review.objects.get(id=self.kwargs['pk'])
      return super (ReplyCreateView, self).form_valid(form)
class ReplyUpdateView(UpdateView):
    model = Reply
    pk_url_kwarg = 'reply_pk'
    template_name = 'reply/reply_form.html'
    fields = ['text']

    def get_success_url(self):
        return self.object.review.get_absolute_url()
    def get_object(self, *args, **kwargs):
        object = super(AnswerUpdateView, self).get_object(*args, **kwargs)
        if object.user != self.request.user:
            raise PermissionDenied()
        return object

class ReplyDeleteView(DeleteView):
    model = Reply
    pk_url_kwarg = 'reply_pk'
    template_name = 'reply/reply_confirm_delete.html'

    def get_success_url(self):
        return self.object.question.get_absolute_url()
    def get_object(self, *args, **kwargs):
        object = super(ReplyDeleteView, self).get_object(*args, **kwargs)
        if object.user != self.request.user:
            raise PermissionDenied()
        return object


