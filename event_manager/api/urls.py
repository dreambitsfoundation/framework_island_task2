from django.urls import path
from .views import EventRegistrationView, EventViewSet, RegistrationOnEventsView

urlpatterns = [
    path('event/', EventViewSet.as_view({'get': 'list', 'post': 'create'}), name='event_viewset'),
    path('event/<str:pk>/', EventViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='event_views_individual_record'),
    path('event_registration/', EventRegistrationView.as_view({'get': 'list', 'post': 'create'}), name='event_registration_views'),
    path('event_registration/<str:pk>', EventRegistrationView.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='event_registration_views_individual_record'),
    path('registrations_per_event/<str:pk>', RegistrationOnEventsView.as_view({'get': 'list'}, name="registrations_on_event"))
]