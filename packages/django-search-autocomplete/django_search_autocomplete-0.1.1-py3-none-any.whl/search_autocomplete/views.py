from django.http import JsonResponse
from django.db.models import Q
from django.apps import apps
from django.views.generic import View, TemplateView
from django.shortcuts import render
from django.http import Http404
from .forms import SearchConfigForm

class SearchConfigView(TemplateView):
    template_name = 'search_autocomplete/config.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = SearchConfigForm(self.request.GET or None)
        
        if form.is_valid():
            model_label = form.cleaned_data['model']
            form.fields['search_fields'].choices = form.get_model_fields(model_label)
            form.fields['display_fields'].choices = form.get_model_fields(model_label)
            
        context['form'] = form
        return context

class GenericSearchView(View):
    def get(self, request):
        model_label = request.GET.get('model')
        search_fields = request.GET.getlist('search_fields')
        display_fields = request.GET.getlist('display_fields')
        max_results = int(request.GET.get('max_results', 5))
        query = request.GET.get('query', '')

        if not all([model_label, search_fields, display_fields]):
            return JsonResponse({'error': 'Missing required parameters'}, status=400)

        try:
            app_label, model_name = model_label.split('.')
            model = apps.get_model(app_label, model_name)
        except (ValueError, LookupError):
            return JsonResponse({'error': 'Invalid model'}, status=400)

        if len(query) < 2:
            return JsonResponse({'results': []})

        # Build the search query
        search_query = Q()
        for field in search_fields:
            search_query |= Q(**{f"{field}__icontains": query})

        # Get and filter results
        queryset = model.objects.filter(search_query)[:max_results]
        
        # Format results
        formatted_results = []
        for obj in queryset:
            result = {}
            for field in display_fields:
                try:
                    # Handle foreign key string representation
                    if field.endswith('__str'):
                        field_name = field[:-5]
                        value = str(getattr(obj, field_name))
                    else:
                        value = getattr(obj, field)
                        # Handle file/image fields
                        if hasattr(value, 'url'):
                            value = value.url
                        else:
                            value = str(value)
                    result[field] = value
                except (AttributeError, ValueError):
                    continue
            formatted_results.append(result)

        return JsonResponse({'results': formatted_results})

class SearchAutocompleteView(View):
    """
    A generic view for handling search autocomplete functionality.
    For backward compatibility.
    """
    model = None
    search_fields = []
    result_fields = []
    image_field = None
    price_field = None
    discount_field = None
    max_results = 5
    
    def get_queryset(self):
        return self.model.objects.all()
    
    def format_result(self, obj):
        result = {}
        for field in self.result_fields:
            if hasattr(obj, field):
                result[field] = getattr(obj, field)
        
        if self.image_field and hasattr(obj, self.image_field):
            image = getattr(obj, self.image_field)
            result['image'] = image.url if hasattr(image, 'url') else image
        
        if self.price_field and hasattr(obj, self.price_field):
            price = getattr(obj, self.price_field)
            result['price'] = str(price)
            
            if self.discount_field and hasattr(obj, self.discount_field):
                discount = getattr(obj, self.discount_field)
                if discount:
                    discounted_price = price * (1 - discount / 100) if discount else price
                    result['discounted_price'] = str(discounted_price)
        
        return result
    
    def get(self, request):
        query = request.GET.get('query', '')
        if len(query) < 2:
            return JsonResponse({'results': []})
        
        search_query = Q()
        for field in self.search_fields:
            search_query |= Q(**{f"{field}__icontains": query})
        
        queryset = self.get_queryset()
        results = queryset.filter(search_query)[:self.max_results]
        formatted_results = [self.format_result(obj) for obj in results]
        
        return JsonResponse({'results': formatted_results}) 