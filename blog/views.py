from django.shortcuts import render, get_object_or_404
from blog.models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from blog.forms import ShareByEmailForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag


def post_list_view(request, tag_slug=None):
    post = Post.list_objects.all()
    # tag_slug=None
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post = Post.objects.filter(tags__in=[tag])
   
    paginator = Paginator(post, 3)
    page_number = request.GET.get('page')
    
    try:
        post = paginator.page(page_number)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    print(type(post))
    return render(request, 'blog/post_list.html', {'post_list': post, 'tag':tag})

def post_detail_view(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    csubmit = False
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            csubmit = True
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post':post, 'form':form, 'csubmit':csubmit, 
                'comments':comments})


def shareByEmail(request, id):
    post = get_object_or_404(Post, id=id)
    form = ShareByEmailForm()
    if request.method == 'POST':
        form = ShareByEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['to_email']
            blog_link =  request.build_absolute_uri(post.get_absolute_url())
            print(blog_link)
            subject = 'Your friend "{}" recommended you to read ->"{}" '.format(form.cleaned_data['username'], post.title)
            send_mail(subject, blog_link, None, [email, ], fail_silently=False)
            sent = True
            return render(request, 'blog/sharebyemail.html', {'sent':sent})
    return render(request, 'blog/sharebyemail.html', {'form':form, 'post':post})
