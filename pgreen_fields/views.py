from __future__ import absolute_import

from django.views import generic
from django.views.generic.edit import CreateView, ProcessFormView
from django.core.urlresolvers import reverse_lazy

from .models import SolarPanel
from .forms import CrispySolarPanelForm #SolarPanelForm


class SolarPanelListView(generic.ListView):

    model = SolarPanel 
    http_method_names = ['get', 'post'] 

    def get_queryset(self): 
        queryset = super(SolarPanelListView, self).get_queryset()
        return queryset


class SolarPanelDetailView(generic.DetailView):

    http_method_names = ['get', 'post']
    form_class = CrispySolarPanelForm
    model = SolarPanel 

    def get_queryset(self):
        return self.model.objects


class SolarPanelCreateView(CreateView, ProcessFormView):

    form_class = CrispySolarPanelForm
    model = SolarPanel
    exclude = ('slug',) 
    success_url = reverse_lazy('SolarPanel-home')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super(SolarPanelCreateView, self).form_valid(form)


class SolarPanelUpdateView(generic.UpdateView):

    http_method_names = ['get', 'post']
    form_class = CrispySolarPanelForm
    model = SolarPanel 
    exclude = ('slug',)
    success_url = reverse_lazy('SolarPanel-home')