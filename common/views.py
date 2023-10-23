from django.shortcuts import render
import folium

def index(request):
    m = folium.Map(location=[4.142, -73.62664], zoom_start=13)
    context = {'map': m._repr_html_()}
    return render(request, "index.html", context)

def login(request):
    return render(request, "login.html")
