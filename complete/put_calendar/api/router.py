

from put_calendar.api.viewsets import CalendarViewSet

from rest_framework  import routers

router = routers.DefaultRouter()
router.register('put_calendar_api',CalendarViewSet,base_name='put_calendar_api')
