from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.generic import ListView
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail

# Create your views here.
# def post_list(request):
#     object_list = Post.published.all()
#     paginator = Paginator(object_list,3) #3 Post per page
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         #If page number is not an int return first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     context = {
#         'page': page,
#         'posts': posts,
#     }
#     return render(request,'Blog/post/list.html', context)

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 5
    template_name = 'Blog/post/list.html'

def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year = year,
    publish__month = month, publish__day = day)
    comments = post.comments.filter(active = True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    context = {
        'post':post,
        'comments':comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }
    return render(request, 'Blog/post/detail.html', context)

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="published")
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST) #Form was submitted
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            #send _email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd["name"]}({cd["email"]}) recommends you reading "{post.title}"'
            message = f'Read "{post.title}" at {post_url}\n\n{cd["name"]}\'s comments:{cd["comments"]}'
            send_mail(subject,message,'preetshah964@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    context = {
        'post':post,
        'form':form,
        'sent': sent,
    }
    return render(request,'Blog/post/share.html', context)
    