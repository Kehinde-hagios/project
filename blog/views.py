from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def home(request):
    posts = Post.objects.all().order_by('-updated_at')
    return render(request, 'blog/home.html', {'posts': posts})


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-updated_at']
    paginate_by = 5
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/view.html'
    
class ProfileView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-updated_at')
    
 
class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    template_name = 'blog/create.html'
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin ,UpdateView):
    model = Post
    template_name = 'blog/create.html'
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin ,DeleteView):
    model = Post
    template_name = 'blog/delete.html'
    success_url = '/'   

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
