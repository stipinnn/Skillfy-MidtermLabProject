from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.views.generic.edit import UpdateView, DeleteView

class PostListView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm()
        return render(request, 'social/post_list.html', {'post_list': posts, 'form': form})

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('post-list')  # Redirect to the URL named 'post-list'

        posts = Post.objects.all().order_by('-created_on')
        return render(request, 'social/post_list.html', {'post_list': posts, 'form': form})
    
class PostDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        
        comments = Comment.objects.filter(post=post).order_by('created_on')
        
        context = {
            'post': post,
            'form': form,
            'comments' : comments,
        }
        
        return render(request, 'social/post_detail.html', context)
    def post (self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)
        
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            
        comments = Comment.objects.filter(post=post).order_by('created_on')
        
        context = {
            'post': post,
            'form': form,
            'comments' : comments,
        }
        
        return render(request, 'social/post_detail.html', context)
    
class PostEditView(UpdateView):
     model = Post
     fields = ['body']
     template_name = 'social/post_edit.html'
     
     def get_success_url(self):
         pk = self.kwargs['pk']
         return reverse_lazy ('post-detail', kwargs={'pk':pk})

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'social/post_delete.html'
    success_url = reverse_lazy('post-list')
       
