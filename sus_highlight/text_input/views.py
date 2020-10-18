from django.views import generic
from django.urls import reverse_lazy
from .forms import TOSInputForm
import re
from . import textClassification

def create_clean_list_of_strings(s):
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
    return list_of_strings

class IndexView(generic.FormView):
    template_name = 'text_input/index.html'
    form_class = TOSInputForm
    success_url = reverse_lazy('text_input:highlight')

    def form_valid(self, form):
        list_of_strings = create_clean_list_of_strings(form.cleaned_data['terms_of_service'])
        list_of_dictionaries = textClassification.getClass(list_of_strings)
        self.request.session['tos_list_of_dicts'] = list_of_dictionaries 
        return super().form_valid(form)

class HighlightView(generic.TemplateView):
    template_name = 'text_input/highlight.html'