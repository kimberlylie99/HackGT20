from django.views import generic
from django.urls import reverse_lazy
from .forms import TOSInputForm
import re

class IndexView(generic.FormView):
    template_name = 'text_input/index.html'
    form_class = TOSInputForm
    success_url = reverse_lazy('text_input:highlight')

    def form_valid(self, form):
        s = form.cleaned_data['terms_of_service']
        print(s)
        # Replace newlines with spaces
        s = s.replace('\n', ' ')
        # Replace tabs with spaces
        s = s.replace('\t', ' ')
        # Replace returns with spaces
        s = s.replace('\r', ' ')
        # Replace multiple spaces in a row with one space
        s = re.sub(' +', ' ', s)
        # Remove leading and trailing whitespace
        s = s.strip()
        # Split into list of strings on periods, but keep in the periods.
        list_of_strings = re.findall('[^\.]+\.', s)
        print(list_of_strings)
        self.request.session['terms_of_service'] = s
        return super().form_valid(form)

class HighlightView(generic.TemplateView):
    template_name = 'text_input/highlight.html'