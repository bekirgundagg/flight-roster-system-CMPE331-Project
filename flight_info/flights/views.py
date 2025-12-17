from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
# Model ve Serializer'larını import ediyoruz
from .models import Flight, Airport, VehicleType
from .serializers import FlightSerializer, AirportSerializer, VehicleTypeSerializer
from passengers.models import Passenger
from passengers.serializers import PassengerSerializer
from main_system.services import create_roster_for_flight
from main_system.models import FlightRoster


# NOT: 'flights_list' fonksiyonunu sildim çünkü React projesinde
# HTML template render etmeye (render request...) ihtiyacımız yok.
# O hata da bu yüzden gidip, kodun temizlenmiş oldu.

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAuthenticated]


class VehicleTypeViewSet(viewsets.ModelViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer
    permission_classes = [IsAuthenticated]


class FlightViewSet(viewsets.ModelViewSet):
    # --- DÜZELTME 1: select_related ---
    # Hata mesajında Django dedi ki: "Choices are: source, destination, vehicle"
    # Biz de inatlaşmıyoruz, onun dediği isimleri yazıyoruz.
    queryset = Flight.objects.select_related('source', 'destination', 'vehicle').all()

    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticated]

    # --- DÜZELTME 2: Filtreleme ---
    # Filtrelerde de modeldeki isimleri kullanmalıyız.
    # source_airport__code -> source__code
    filterset_fields = ('flight_number', 'source__code', 'destination__code', 'departure_datetime')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def auto_assign_crew(request, flight_number):
    """
    Frontend'deki 'Otomatik Ata' butonuna basınca çalışır.
    Senin yazdığın create_roster_for_flight fonksiyonunu tetikler.
    """
    try:
        # Flight number (HB0001) verip ID'sini (1, 2 vs) buluyoruz
        flight = Flight.objects.get(flight_number=flight_number)
    except Flight.DoesNotExist:
        return Response({"error": "Uçuş bulunamadı"}, status=404)

    # --- SENİN ALGORİTMANI ÇAĞIRIYORUZ ---
    try:
        result = create_roster_for_flight(flight.id)
    except Exception as e:
        return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)

    # create_roster_for_flight fonksiyonun hata durumunda string dönüyor
    if isinstance(result, str):
        return Response({"error": result}, status=HTTP_400_BAD_REQUEST)

    # Başarılıysa Roster objesi döner
    return Response({
        "message": "Otomatik atama ve koltuk yerleşimi başarıyla tamamlandı!",
        "status": "success"
    }, status=HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_flight_roster(request, flight_number):
    """
    Sayfa açılınca verileri getirir.
    Artık veriyi Flight modelinden değil, varsa FlightRoster modelinden çekeceğiz.
    """
    try:
        flight = Flight.objects.get(flight_number=flight_number)
    except Flight.DoesNotExist:
        return Response({"error": "Uçuş bulunamadı"}, status=404)

    # Yolcuları her zaman getir (Senin kodun koltuklarını güncellemiş olacak)
    passengers = Passenger.objects.filter(flight_id=flight_number)

    crew_data = []
    menu_data = []

    # 1. Bu uçuş için oluşturulmuş bir Roster var mı?
    try:
        # FlightRoster modelinde flight alanına göre arıyoruz
        roster = FlightRoster.objects.get(flight=flight)

        # VARSA: Senin Roster modelinden verileri çekiyoruz

        # A) Pilotlar
        for pilot in roster.pilots.all():
            crew_data.append({
                "id": pilot.id,
                "name": pilot.name,
                "type": "Pilot",
                "role": pilot.seniority_level,
                "avatar": "👨‍✈️"
            })

        # B) Kabin Ekibi
        for member in roster.cabin_crew.all():
            crew_data.append({
                "id": member.attendant_id,
                "name": member.name,
                "type": "Cabin Crew",
                "role": member.attendant_type,
                "avatar": "💁‍♀️"  # veya "👔"
            })
        if roster.menu:
            menu_data = roster.menu

    except FlightRoster.DoesNotExist:
        # Roster henüz oluşturulmamışsa boş liste döner
        pass

    return Response({
        "flight": FlightSerializer(flight).data,
        "passengers": PassengerSerializer(passengers, many=True).data,
        "crew": crew_data,
        "menu": menu_data
    })