from django.shortcuts import render, get_object_or_404, redirect
from .models import MediaEvent, MediaPhoto
from .forms import MultiUploadForm


from django.core.paginator import Paginator


def media_list(request):
    events = MediaEvent.objects.all()
    paginator = Paginator(events, 9)  # 9 карточек на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'media/media_list.html', {'page_obj': page_obj})




def media_detail(request, pk):
    event = get_object_or_404(MediaEvent, pk=pk)
    photos = event.photos.all()  # <-- обращаемся через related_name 'photos'
    return render(request, 'media/media_detail.html', {
        'event': event,
        'photos': photos
    })


def upload_photos(request, pk):
    event = get_object_or_404(MediaEvent, pk=pk)

    if request.method == 'POST':
        form = MultiUploadForm(request.POST, request.FILES)

        if form.is_valid():
            files = request.FILES.getlist('images')
            for f in files:
                MediaPhoto.objects.create(event=event, image=f)

    return redirect('media_detail', pk=pk)