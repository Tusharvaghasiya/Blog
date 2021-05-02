from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from blog.forms import ShareByEmailForm, CommentForm, SignUpForm, PostCreateForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.defaultfilters import slugify
from verify_email.email_handler import send_verification_email
from django.db.models import Count

def about(request):
    return render(request, 'blog/about.html')


def createPost(request):
    form = PostCreateForm()
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        print(request.POST)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.author = request.user
            updated.slug = slugify(updated.title)
            updated.save()
            form.save_m2m()
            return redirect('/')
    return render(request, 'blog/post_create.html', {'form': form})

def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.email = form.cleaned_data['email']
            form.save(commit=False)
            inactive_user = send_verification_email(request, form)
            messages.add_message(request, messages.SUCCESS, 'A verification link has been sent to your email')
            return redirect('login')
            # form.save()

    return render(request, 'blog/signup.html', {'form': form})


def post_list_view(request, tag_slug=None):
    post = Post.list_objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post = Post.objects.filter(tags__in=[tag])
    # print('-'*20)
    # print(request.GET)
    # print(request.POST)
    # print('-'*20)
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

@login_required
def post_detail_view(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # post_tags_ids = post.tags.values_list('id', flat=True)
    # print(len(post_tags_ids))
    # similar_post = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # print(similar_post[0].title)
    # similar_post = similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags', 'publish')[:4]

    post_tags_ids=post.tags.values_list('id',flat=True)
    print(post_tags_ids)
    similar_posts=Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    print(len(similar_posts))
    similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','publish')[:4]
    



    comments = post.comments.filter(active=True)
    csubmit = False
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            csubmit = True
            messages.add_message(request, messages.SUCCESS, 'Comment Submitted!')
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post':post, 'similar_post': similar_posts, 'form':form, 'csubmit':csubmit,
                'comments':comments})


@login_required
def shareByEmail(request, id):
    post = get_object_or_404(Post, id=id)
    form = ShareByEmailForm()
    if request.method == 'POST':
        form = ShareByEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['to_email']
            blog_link =  request.build_absolute_uri(post.get_absolute_url())
            username = request.user.username
            subject = 'Your friend "{}" recommended you to read ->"{}" '.format(username, post.title)
            send_mail(subject, blog_link, None, [email, ], fail_silently=False)
            sent = True
            return render(request, 'blog/sharebyemail.html', {'sent':sent})
    return render(request, 'blog/sharebyemail.html', {'form':form, 'post':post})
