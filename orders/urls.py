from django.urls import path
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_view
from django.views.generic.base import TemplateView
from django_registration.backends.one_step.views import RegistrationView
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='Index'),
    path('index', views.index, name='Index'),
    path('cart', views.cart,  name='View Card'),
    path('confirm-order', views.confirmOrder),
    path(r'add-to-card/<int:menu_id>/', views.addToCard),
    path('dashboard', views.dashboard),
    path('dashboard/edit', views.dashboardEdit),
    path('dashboard/menu', views.dashboardMenu, name='Edit your Menu Items'),
    path('dashboard/orders', views.dashboardOrders),
    path(r'dashboard-accept-order/<int:orderId>', views.dashboardAcceptOrder),
    path(r'dashboard-reject-order/<int:orderId>', views.dashboardRejectOrder),
    path(r'profile/<int:profileId>', views.viewProfile),
    path('give-feedback', views.giveFeedback),
    path(r'delete-menu-item/<int:itemId>', views.dashboarDeleteMenuItem),
    path('dashboard/add-new-item', views.dashboarAddItem),
    path(r'delete-item/<int:orderId>/<int:itemId>/', views.deleteMenuItem),
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
