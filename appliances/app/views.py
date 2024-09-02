from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, LoginForm, ReviewForm
from .models import Product, Category, Review
from django.urls import reverse
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Review, ReviewReaction




def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please check the form and try again.')
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {username}!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('index')

def auto_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return JsonResponse({'status': 'logged out'})


def index(request):
    return render(request, 'index.html')

def product_list_by_category(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    
    return render(request, 'products.html', {
        'products': products,
        'categories': categories,
        'current_category': category,
    })

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'products.html', {'products': products, 'categories': categories})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = Review.objects.filter(product=product).order_by('-created_at')[:6]
    form = None

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(request, 'Review submitted successfully.')
                return redirect('product_detail', slug=product.slug)
        else:
            form = ReviewForm()

    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
    })

def product_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product).order_by('-created_at')[:6]
    
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Review submitted successfully.')
            return redirect('product_review', product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, 'review.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
    })

def like_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    reaction, created = ReviewReaction.objects.get_or_create(user=request.user, review=review)

    if not created and reaction.is_liked:
        return JsonResponse({'error': 'You have already liked this review.'}, status=400)

    if not created and not reaction.is_liked:
        # Change dislike to like
        reaction.is_liked = True
        review.dislike_count -= 1

    review.like_count += 1
    review.save()
    reaction.is_liked = True
    reaction.save()
    return JsonResponse({'like_count': review.like_count})

def dislike_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    reaction, created = ReviewReaction.objects.get_or_create(user=request.user, review=review)

    if not created and not reaction.is_liked:
        return JsonResponse({'error': 'You have already disliked this review.'}, status=400)

    if not created and reaction.is_liked:
        # Change like to dislike
        reaction.is_liked = False
        review.like_count -= 1

    review.dislike_count += 1
    review.save()
    reaction.is_liked = False
    reaction.save()
    return JsonResponse({'dislike_count': review.dislike_count})

def about(request):
    return render(request, 'about.html')

def addToCart(request):
    return render(request, 'addToCart.html')

def contact(request):
    return render(request, 'contact.html')

def developerContact(request):
    return render(request, 'developerContact.html')

def payment(request):
    return render(request, 'payment.html')
def review(request):
    return render(request,'review.html')