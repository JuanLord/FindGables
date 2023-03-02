from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.list import ListView
from .models import Task, Location
from django.core import serializers
from django.template import RequestContext
from django.template.defaulttags import register
import json

from base.scripts.ChatBot.chat_botANN import Chatbot

print("EFE")
# Create your views here.
class TaskList(ListView):
    model = Task
    context_object_name = "tasks" # Name on HTML

def index(request):
    """if request.method == 'POST' and 'run_script' in request.POST:
        # call function
        chaty = Chatbot()
        print(Chatbot.Talking(chaty,"podemos intercambiar mi auto mas nuevo que hay?"))"""

    return render(request, "base/index.html")


def about(request):
    return render(request, "base/about.html")

def attractions(request):
    if request.method == 'POST' and 'run_script' in request.POST:
        # call function that addes activity to session
        print("EEE")
        place_name = request.POST.get("place")
        is_found = False
        if 'location' in request.session:
            print("IF1")
            for loc in request.session['location']:
                print("IF2")
                if place_name in loc["pk"]:
                    print("IF3")
                    # Already on session
                    is_found = True

            if is_found == False:
                print("E")
                location_data = Location.objects.get(name=place_name)
                loc_json =  serializers.serialize('json', [location_data])
                    
                request.session['location'] += json.loads(loc_json)

            if place_name in request.session['location']:
                print("IF5")
                pass   
        else:
            print("IF6")
            request.session['location'] = []
            print("O")
            location_data = Location.objects.get(name=place_name)
            loc_json =  serializers.serialize('json', [location_data])
                
            request.session['location'] += json.loads(loc_json)

        
    json_serializer = serializers.get_serializer("json")()
    my_data = json_serializer.serialize(Location.objects.all(), ensure_ascii=False)
    locs = Location.objects.all()
    try:
        request.session['location']
    except:
        context = {"place":my_data,"data":locs}
    else:
        context = {"place":my_data,"data":locs, "location":request.session['location']}
        
    
    
    return render(request, "base/attractions.html", context)
    #return render(request, "base/attractions.html", context)

def itinerary(request):
    total = len(request.session['location'])
    days = round((total + 1) / 3)
    print(f"{days} {total}")
    print(request.session['location'])
    context = {"total":total,"days":days, "locations":request.session['location']}
    #request.session
    return render(request, "base/itinerary.html",{"total":total,"days":days,"locations":request.session['location']})

def location(request, name):
    location_data = Location.objects.get(name=name)
    
    loc_json =  serializers.serialize('json', [location_data])

    request.session['location'] = [json.loads(loc_json)]
    
    """if 'name' in request.session:
        if name in request.session['name']:
            request.session['name'].remove(name)

        print(request.session['name'])
        location_saved = Location.objects.filter(pk=request.session['name'])
        request.session['name'].insert(0,name)
        if len(request.session['name']) > 5:
            request.session['name'].pop()
        #request.session['name']
    else:
        request.session['name'] = [name]"""

    request.session.modified = True
        
    #context = {'location_saved':json.dumps(request.session['location'][0][0]["fields"]["ages"])}
    
    #print("LOCATION: "+f"{request.session['location'][0][0]['fields']['ages']}")
    data = request.session['location'][0][0]['fields']
    print(data)
    return render(request, "base/location.html", {"image":data['image'], "open":data["openhours"], "address":data["address"],"cost":data["price"],"description":data['description'],"name":request.session['location'][0][0]['pk']})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
def functions(request):
    print(request.GET.get('var'))
    chaty = Chatbot()
    response = (Chatbot.Talking(chaty,request.GET.get('var')))
    return JsonResponse({"text":response[0]})

def map(request):
    json_serializer = serializers.get_serializer("json")()
    my_data = json_serializer.serialize(Location.objects.all(), ensure_ascii=False)
    locs = Location.objects.all()
    context = {"place":my_data,"data":locs}
    
    return render(request, "base/chaty.html", context)

def send_message(request):
  # Check if the request is POST
  if request.method == "POST":
    # Get the message from the request data
    message = request.POST.get("message")

    # Do something with the message (e.g. save it to database)

    # Return a JSON response with some feedback
    return JsonResponse({"message": f"You sent: {message}"})

  # If not POST, return an error response
  else:
   return JsonResponse({"error": "Invalid request method"})
  
@register.filter(name='get_item')
def get_item(dictionary, key):
    print(f"DICTIY   {dictionary} DICTYIII {key}")
    return key