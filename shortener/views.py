from django.shortcuts import render

# Create your views here.
import string
import random
from django.shortcuts import render, redirect, get_object_or_404
from .models import ShortenedURL

def generate_short_code():
    """Generate a random 6-character string."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def shorten_url(request):
    if request.method == 'POST':
        original_url = request.POST['original_url']
        # Check if the URL already exists
        url, created = ShortenedURL.objects.get_or_create(original_url=original_url)
        if created:
            url.short_code = generate_short_code()
            url.save()
        return render(request, 'shortener/shorten_url.html', {'short_url': request.build_absolute_uri(url.short_code)})
    return render(request, 'shortener/shorten_url.html')

def redirect_to_original(request, short_code):
    url = get_object_or_404(ShortenedURL, short_code=short_code)
    return redirect(url.original_url)
