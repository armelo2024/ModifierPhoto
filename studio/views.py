from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
from django.http import HttpResponseForbidden
from .forms import UploadForm
from .models import Photo
from .processing import remove_background_and_apply_color
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.


# Home space
def home(request):
    return render(request, 'home.html')

# Studio space
def studio(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data["image"]
            bg_color = form.cleaned_data["bg_color"]
            transparent = form.cleaned_data["is_transparent"]

            photo = Photo.objects.create(
                owner=request.user if request.user.is_authenticated else None,
                original_image=img,
                bg_color=bg_color,
                is_transparent=transparent,
                status="pending",
            )

            try:
                out_bytes, fmt = remove_background_and_apply_color(img, bg_color, transparent)
                filename = f"{photo.id}.{'png' if transparent else 'jpg'}"
                photo.processed_image.save(filename, ContentFile(out_bytes.read()))
                photo.status = "done"
            except Exception as e:
                photo.status = "error"
                photo.error_message = str(e)

            photo.save()
            return redirect("gallery")
    else:
        form = UploadForm()

    return render(request, "studio.html", {"form": form})

# Gallery space

def gallery(request):
    photos_list = Photo.objects.filter(status="done").order_by("-created_at")
    paginator = Paginator(photos_list, 6)  # ✅ 6 photos par page

    page_number = request.GET.get("page")
    photos = paginator.get_page(page_number)  # Retourne un objet Page

    return render(request, "gallery.html", {"photos": photos})


# Photo_detail space
def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if photo.owner and request.user != photo.owner:
        return HttpResponseForbidden()
    return render(request, "photo_detail.html", {"photo": photo})

def photo_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if photo.owner and request.user != photo.owner:
        return HttpResponseForbidden()
    if request.method == "POST":
        photo.delete()
        messages.success(request, "Photo supprimée avec succès.")
        return redirect("gallery")
    return render(request, "photo_delete.html", {"photo": photo})