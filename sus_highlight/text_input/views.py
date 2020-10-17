from django.views import generic
from django.urls import reverse_lazy
from .forms import TOSInputForm

class IndexView(generic.FormView):
    template_name = 'text_input/index.html'
    form_class = TOSInputForm
    success_url = reverse_lazy('text_input:highlight')

    def form_valid(self, form):
        self.request.session['terms_of_service'] = form.cleaned_data['terms_of_service']
        return super().form_valid(form)

class HighlightView(generic.TemplateView):
    template_name = 'text_input/highlight.html'