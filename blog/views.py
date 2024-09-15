from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import SingleObjectMixin


class HomeView(generic.View):
     # model = Post
    template_name = 'home.html'
    paginate_by = 4

    def get(self, request):
        posts = Post.objects.all()
        paginator = Paginator(posts, self.paginate_by)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'post_list': page_obj
        }

        return render(request, self.template_name, context)



class PostDetailView(generic.View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)



class PostNewView(generic.CreateView):
    model = Post
    template_name = 'post_new.html'
    form_class = PostForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)


class PostUpdateView(generic.edit.UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title', 'excerpt', 'body', 'photo']



class PostDeleteView(generic.edit.DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')




class CommentGet(generic.DetailView):
    model = Post
    template_name = 'post_single.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context
    

class CommentPost(SingleObjectMixin, generic.FormView):
    model = Post
    form_class = CommentForm
    template_name = "post_single.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        post = self.get_object()
        return reverse("post-detail", kwargs={'pk': post.pk})