from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Image, Category
from .forms import ImageUploadForm
from PIL import Image as PILImage
from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
from django.contrib import messages
from io import BytesIO
import asyncio
from django.http import StreamingHttpResponse
from asgiref.sync import sync_to_async


def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def image_upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            messages.success(request, "Image uploaded successfully")
            return redirect('image_list')
    else:
        form = ImageUploadForm()
    return render(request, 'images/upload_image.html', {'form': form})

def image_list(request):
    category_id = request.GET.get('category')
    query = request.GET.get('q')

    images = Image.objects.all().order_by('-id')  # Order by newest first

    if category_id:
        images = images.filter(categories__id=category_id)

    if query:
        images = images.filter(title__icontains=query)

    categories = Category.objects.all()

    paginator = Paginator(images, 24)  # Show 24 images per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'images/image_list.html', {'page_obj': page_obj, 'categories': categories})

def image_detail(request, pk):
    image = get_object_or_404(Image, pk=pk)
    related_images = Image.objects.filter(categories__in=image.categories.all()).exclude(pk=pk).distinct().order_by('?')[:4]
    resolutions = [
        (1920, 1080),
        (1280, 720),
        (3840, 2160),
        (5120, 2880),
    ]
    return render(request, 'images/image_detail.html', {
        'image': image,
        'related_images': related_images,
        'resolutions': resolutions,
    })

def file_iterator(img, format):
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format=format)
    img_byte_arr.seek(0)
    while True:
        chunk = img_byte_arr.read(8192)
        if not chunk:
            break
        yield chunk

async def async_file_iterator(img, format):
    for chunk in file_iterator(img, format):
        yield chunk
        await asyncio.sleep(0)  # Allow other tasks to run

async def download_image(request, pk, width, height):
    image = await sync_to_async(get_object_or_404)(Image, pk=pk)
    
    try:
        # Open the image file
        with default_storage.open(image.image.name, 'rb') as f:
            img = PILImage.open(f)
        
        # Process the image
        img = img.resize((width, height), PILImage.LANCZOS)
        
        # Prepare the response
        response = StreamingHttpResponse(async_file_iterator(img, 'JPEG'), content_type="image/jpeg")
        response['Content-Disposition'] = f'attachment; filename="{image.title}_{width}x{height}.jpg"'
        return response
    except Exception as e:
        messages.error(request, f"Error downloading image: {str(e)}")
        return redirect('image_detail', pk=pk)