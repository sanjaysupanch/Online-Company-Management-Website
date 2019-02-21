from put_calendar.models import check_date,check_date1
from .serializers import calendarserializer

from rest_framework import viewsets

from rest_framework.response import Response

from rest_framework.decorators import action


class CalendarViewSet(viewsets.ModelViewSet):

    # we have methods called list ,create , retrieve,update, partial_update

    queryset = check_date1.objects.all()
    serializer_class= calendarserializer

    @action(methods=['get'], detail=False)
    def newest(self,request):

        newest= self.get_queryset().last()

        serializer=self.get_serializer_class()(newest)

        return Response(serializer.data)
