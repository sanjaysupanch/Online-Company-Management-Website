from django import forms
from put_calendar.models import check_date
import datetime

MONTHS = (
    ( 1, 'January'),
    ( 2, 'February'),
    ( 3, 'March'),
    ( 4, 'April'),
    ( 5, 'May'),
    ( 6, 'June'),
    ( 7, 'July'),
    ( 8, 'August'),
    ( 9, 'September'),
    ( 10, 'October'),
    ( 11, 'November'),
    ( 12, 'December'),
)

class check_dateform(forms.ModelForm):

    class Meta:
        model=check_date
        fields=(
            'work_title',
        )


class choose_month_and_year_form(forms.Form):

	month=forms.ChoiceField(choices=MONTHS)
	year = forms.ChoiceField(choices=[(x, x) for x in range(1950, 3000)],initial=2019)
