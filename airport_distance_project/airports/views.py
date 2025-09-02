from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import AirportDistanceForm
from geopy.distance import geodesic
import json

# --- Vista principal ---

def airport_distance_view(request):
    """Renderiza la página principal con el formulario."""
    form = AirportDistanceForm()
    return render(request, "airport_distance.html", {"form": form})

# --- Lógica de la calculadora ---

# Simulación de una base de datos o API de aeropuertos.
# En una aplicación real, esto vendría de una base de datos.
AIRPORT_DATA = {
    "BOG": {"name": "Aeropuerto Internacional El Dorado", "coords": (4.70159, -74.1469)},
    "MEX": {"name": "Aeropuerto Internacional de la Ciudad de México", "coords": (19.4363, -99.0721)},
    "JFK": {"name": "John F. Kennedy International Airport", "coords": (40.6413, -73.7781)},
    "MAD": {"name": "Aeropuerto Adolfo Suárez Madrid-Barajas", "coords": (40.4983, -3.5676)},
    "MIA": {"name": "Miami International Airport", "coords": (25.7959, -80.2871)},
    "LAX": {"name": "Los Angeles International Airport", "coords": (33.9416, -118.4085)},
}

@require_POST
def calculate_distance(request):
    """
    Calcula la distancia entre dos aeropuertos usando datos POST y un formulario de Django.
    """
    form = AirportDistanceForm(request.POST)

    if form.is_valid():
        codigo_origen = form.cleaned_data['aeropuerto_origen']
        codigo_destino = form.cleaned_data['aeropuerto_destino']

        if codigo_origen == codigo_destino:
            return JsonResponse({
                "success": False,
                "error": "El aeropuerto de origen y destino no pueden ser iguales."
            }, status=400)

        origen_data = AIRPORT_DATA.get(codigo_origen)
        destino_data = AIRPORT_DATA.get(codigo_destino)

        if not origen_data:
            return JsonResponse({"success": False, "error": f"Código de origen no encontrado: {codigo_origen}"}, status=404)
        if not destino_data:
            return JsonResponse({"success": False, "error": f"Código de destino no encontrado: {codigo_destino}"}, status=404)

        distancia = geodesic(origen_data["coords"], destino_data["coords"]).kilometers

        return JsonResponse({
            "success": True,
            "aeropuerto_origen": {
                "codigo": codigo_origen,
                "nombre": origen_data["name"]
            },
            "aeropuerto_destino": {
                "codigo": codigo_destino,
                "nombre": destino_data["name"]
            },
            "distancia_km": round(distancia, 2)
        })
    else:
        # Devuelve los errores de validación del formulario en formato JSON
        return JsonResponse({"success": False, "error": json.loads(form.errors.as_json())}, status=400)