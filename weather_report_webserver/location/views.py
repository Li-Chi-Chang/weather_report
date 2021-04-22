from django.shortcuts import render

# Create your views here.
def main(request):
    from django.shortcuts import render
    from . import models

    locationsinfo = []
    
    for location in models.locations:
        onedata = {}
        onedata['name'] = location
        onedata['link'] = location
        locationsinfo.append(onedata)

    return render(request, 'main.html', {
        'locations': locationsinfo,
    })

def location(request):
    from django.shortcuts import render
    from . import models

    path = request.path[1:]
    
    return render(request, 'location.html', {
        'location': path,
    })