from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Button, Submit 
from crispy_forms.bootstrap import FormActions

from .models import SolarPanel


#DELETE?
class SolarPanelForm(ModelForm):

    class Meta:
        exclude = ('slug',)
        model = SolarPanel


class CrispySolarPanelForm(ModelForm):

    class Meta:
        exclude = ('slug',)
        model = SolarPanel

    def __init__(self, *args, **kwargs):
        super(CrispySolarPanelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'square_feet_access',
            'avail_team_period',
            'types_of_surface',
            'unique_install_parameters',

            FormActions(
            Submit('save', 'Save changes'),
            Button('cancel', 'Cancel')
           )
        )