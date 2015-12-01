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
from django.shortcuts import redirect
from django.views.generic import FormView
from .forms import *
# Create your views here.
class Home(TemplateView):
  template_name = "home.html"

class ReviewCreateView(CreateView):
    model = Review
    template_name = "review/review_form.html"
    fields = ['title', 'description', 'visibility']
    success_url = reverse_lazy('review_list')

    def form_valid(self, form):
      form.instance.user = self.request.user
      return super (ReviewCreateView, self).form_valid(form)
class ReviewListView(ListView):
      model = Review
      template_name = "review/review_list.html"
      paginate_by = 5
      
      def get_context_data(self, **kwargs):
        context = super(ReviewListView, self).get_context_data(**kwargs)
        user_votes = Review.objects.filter(vote__user=self.request.user)
        context['user_votes'] = user_votes
        return context
class ReviewDetailView(DetailView):
        model = Review
        template_name = 'review/review_detail.html'
        def get_context_data(self, **kwargs):
          context = super(ReviewDetailView, self).get_context_data(**kwargs)
          review = Review.objects.get(id=self.kwargs['pk'])
          replies = Reply.objects.filter(review=review)
          context['replies'] = replies
          user_votes = Reply.objects.filter(vote__user=self.request.user)
          context['user_votes'] = user_votes
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
                  fields = ['text', 'visibility']

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

class VoteFormView(FormView):
                              form_class = VoteForm

                              def form_valid(self, form):
                                user = self.request.user
                                review = Review.objects.get(pk=form.data["review"])
                                try:
                                  reply = Reply.objects.get(pk=form.data["reply"])
                                  prev_votes = Vote.objects.filter(user=user, reply=reply)
                                  has_voted = (prev_votes.count()>0)
                                  if not has_voted:
                                    Vote.objects.create(user=user, reply=reply)
                                  else:
                                      prev_votes[0].delete()
                                      return redirect(reverse('review_detail', args=[form.data["review"]]))
                                except:
                                      prev_votes = Vote.objects.filter(user=user, review=review)
                                      has_voted = (prev_votes.count()>0)
                                      if not has_voted:
                                        Vote.objects.create(user=user, review=review)
                                else:
                                          prev_votes[0].delete()
                                          return redirect('review_list')

class UserDetailView(DetailView):
  model = User
  slug_field = 'username'
  template_name = 'user/user_detail.html'
  context_object_name = 'user_in_view'

  def get_context_data(self, **kwargs):
    context = super(UserDetailView, self).get_context_data(**kwargs)
    user_in_view = User.objects.get(username=self.kwargs['slug'])
    reviews = Review.objects.filter(user=user_in_view).exclude(visibility=1)
    context['reviews'] = reviews
    replies = Reply.objects.filter(user=user_in_view).exclude(visibility=1)
    context['replies'] = replies
    return context
class UserUpdateView(UpdateView):
  model = User
  slug_field = "username"
  template_name = "user/user_form.html"
  fields = ['email', 'first_name', 'last_name']

  def get_success_url(self):
    return reverse('user_detail', args=[self.request.user.username])

  def get_object(self, *args, **kwargs):
    object = super(UserUpdateView, self).get_object(*args, **kwargs)
    if object !=self.request.user:
      raise PermissionDenied()
    return object
class UserDeleteView(DeleteView):
  model = User
  slug_field = "username"
  template_name = 'user/user_confirm_delete.html'

  def get_success_url(self):
    return reverse_lazy('logout')

  def get_object(self, *args, **kwargs):
    object = super(UserDeleteView, self).get_object(*args, **kwargs)
    if object != self.request.user:
      raise PermissionDenied()
    return object

  def delete(self, request, *args, **kwargs):
    user = super(UserDeleteView, self). get_object(*args)
    user.is_active = False
    user.save()
    return redirect(self.get_success_url())

class SearchReviewListView(ReviewListView):
    def get_queryset(self):
      incoming_query_string = self.request.GET.get('query','')
      return Review.objects.filter(title__icontains=incoming_query_string)


