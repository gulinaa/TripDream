from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from main.forms import DestinationForm
from main.models import Destination, DestinationImage
from order.forms import AddToCartForm


class DestinationsListView(ListView):
    queryset = Destination.objects.all()
    template_name = 'main/destination_list.html'
    context_object_name = 'destinations'
    paginate_by = 2


class DestinationDetailsView(DetailView):
    queryset = Destination.objects.all()
    template_name = 'main/destination_details.html'
    context_object_name = 'destinations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['cart_form'] = AddToCartForm()
        return context


# ImageFormset = models.Formset_factory(ProductImage,
#                                     form=ProductImage,
#                                     extra=3,
#                                     max_num=5,
#                                     can_delete=True)


class IsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_staff


class CreateDestinationView(IsAdminMixin, CreateView):
    queryset = Destination.objects.all()
    template_name = 'main/create_destination.html'
    form_class = DestinationForm
    success_url = reverse_lazy('destination-list')

    def post(self, request, *args, **kwargs):
        self.object = None
        form = DestinationForm(request.POST)
        if form.is_valid():
            destination = form.save()
            for image in request.FILES.getlist('destination_image'):
                print(image)
                DestinationImage.objects.create(destination=destination, image=image)
            return redirect(destination.get_absolute_url())
        return self.form_invalid(form)


class UpdateDestinationView(IsAdminMixin, UpdateView):
    queryset = Destination.objects.all()
    form_class = DestinationForm
    template_name = 'main/update_destination.html'
    context_object_name = 'destination'


class DeleteDestinationView(IsAdminMixin, DeleteView):
    queryset = Destination.objects.all()
    template_name = 'main/delete_destination.html'
    success_url = reverse_lazy('destination-list')


class IndexPageView(TemplateView):
    template_name = 'main/index.html'


class SearchResultsView(View):
    def get(self, request):
        queryset = None
        search_param = request.GET.get('search')
        if search_param is not None:
            queryset = Destination.objects.filter(Q(name__icontains=search_param)|
                                            Q(description__icontains=search_param))
            return render(request, 'main/search.html', {'destinations': queryset})



