from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import FileUploadingView, FilesViewSet


router = DefaultRouter()

router.register('files', FilesViewSet)

urlpatterns = [
    path('upload/', FileUploadingView.as_view()),
    path('', include(router.urls)),
]