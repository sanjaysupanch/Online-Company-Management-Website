from rest_framework import serializers

from put_calendar.models import check_date,check_date1


class calendarserializer(serializers.HyperlinkedModelSerializer):

    class Meta:
         model=check_date1

         fields=(
            'date',
            'work_title',


         )
