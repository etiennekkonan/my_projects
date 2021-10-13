from django.shortcuts import render, get_object_or_404
#from django.http import HttpResponse
#from django.template import loader
#from django.views.decorators.csrf import requires_csrf_token
from .models import Album, Artist, Contact, Booking
from .forms import ContactForm

#from .models import ALBUMS
# Create your views here.

def index(request):
    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
	 # then format the request.
    # note that we don't use album['name'] anymore but album.name
    # because it's now an attribute.
    formatted_albums = ["<li>{}</li>".format(album.title) for album in albums]
    #message = """<ul>{}</ul>""".format("\n".join(formatted_albums))
    #template = loader.get_template('store/index.html')
    context = {
        'albums': albums
    }
    return render(request, 'store/index.html', context)

def listing(request):
    albums = Album.objects.filter(available=True)
    context = {
        'albums': albums
    }

    return render(request, 'store/listing.html', context)

def detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    artists = [artist.name for artist in album.artists.all()]
    artists_name = " ".join(artists)
    context = {
        'album_title': album.title,
        'artists_name': artists_name,
        'album_id': album.id,
        'thumbnail': album.picture
       
    }
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
        try:    
            contact = Contact.objects.filter(email=email)[0]
            
        except:

            contact = Contact.objects.create(
                email=email,
                name=name
            )
           
                # If no album matches the id, it means the form must have been tweaked
        # so returning a 404 is the best solution.
        album = get_object_or_404(Album, id=album_id)
        booking = Booking.objects.create(
            contact=contact,
            album=album
        )

        # Make sure no one can book the album again.
        album.available = False
        album.save()
        context = {
            'album_title': album.title
        }
        return render(request, 'store/merci.html', context)

    else:
        context['errors'] = form.errors.items()

else:
    form = Contactform()

context['form'] = form
            
return render(request, 'store/detail.html', context)

def search(request):

    query = request.GET.get('query')

    if not query:
        album = Album.objects.all()
    else:
        albums = Album.objects.filter(title__icontains=query)

        if not albums.exists():
            albums = Album.objects.filter(artists__name__icontains=query)

    title = "Résultats pour la requête %s"%query

    context = {
        'albums': albums,
        'title': title
    }

    return render(request, 'store/search.html', context)