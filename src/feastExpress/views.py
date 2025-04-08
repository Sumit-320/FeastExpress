from django.shortcuts import HttpResponse,render
from vendor.models import Vendor
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

def init_location(request):
    if 'lat' in request.session:
        lat = request.session['lat']
        lng = request.session['lng']
        return lng,lat
    elif 'lat' in request.GET:
        lat= request.GET.get('lat')
        lng= request.GET.get('lng')
        request.session['lat']=lat
        request.session['lng']=lng
        return lng,lat
    else:
        return None
    
def home(request):
    # queries to bring nearby restaurants to home page radius~5000km
    if init_location(request) is not None:
        pnt = GEOSGeometry('POINT(%s %s)' % (init_location(request))) 
        vendors = Vendor.objects.filter(profile__location__distance_lte=(pnt, D(km=5000))
        ).annotate(distance = Distance("profile__location",pnt)).order_by("distance")

        for v in vendors:
            v.kms = round(v.distance.km,1)
    else:
        vendors=Vendor.objects.filter(is_approved=True,user__is_active = True)[:12]  # user model's is_active
        
    
    context={
        'vendors':vendors,
    }
    return render(request,'home.html',context)

def get_or_set_current_location(request):
    if 'lat' in request.session:
        lat = request.session['lat']
        lng = request.session['lng']
        return lng,lat
    elif 'lat' in request.GET:
        lat= request.GET.get('lat')
        lng= request.GET.get('lng')
        request.session['lat']=lat
        request.session['lng']=lng
        return lng,lat
    else:
        return None