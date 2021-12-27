
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from main.views import IndexPageView
from order.views import ActivationOrderView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexPageView.as_view(), name='index'),
    path('account/', include('account.urls')),
    path('cart/', include('order.urls')),
    path('main/', include('main.urls')),
    path('order/activate/<str:activation_code>/',
    ActivationOrderView.as_view()),
]
#
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

