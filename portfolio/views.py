from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from . models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView , DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from taggit.models import Tag
from django.template.defaultfilters import slugify
from . forms import PostForm

def home(request):
    #context = {
    #'posts': Post.objects.all()
    #}
    posts = Post.objects.order_by('-published')
    # Show most common tags
    common_tags = Post.tags.most_common()[:4]
    form = PostForm(request.POST)
    if form.is_valid():
        newpost = form.save(commit=False)
        newpost.slug = slugify(newpost.title)
        newpost.save()
        # Without this next line the tags won't be saved.
        form.save_m2m()
    context = {
        'posts':posts,
        'common_tags':common_tags,
        'form':form,
    }

    return render(request, 'portfolio/home.html', context)

def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name
    posts = Post.objects.filter(tags=tag)
    context = {
        'tag':tag,
        'posts':posts,
    }
    return render(request, 'portfolio/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'portfolio/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted'] #- for oldest
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'portfolio/user_post.html'
    context_object_name = 'posts'
    ordering = ['-date_posted'] #- for oldest
    paginate_by = 5



    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'header_image', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'portfolio/about.html', {'title':'About'})
