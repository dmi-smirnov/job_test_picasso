from rest_framework import viewsets
from rest_framework.generics import CreateAPIView

from api.models import File
from api.serializers import FileSerializer
from api.tasks import process_file


class FileUploadingView(CreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def perform_create(self, serializer):
        default_result = super().perform_create(serializer)

        orm_created_file = serializer.instance

        # Creating Celery task for processing file
        process_file.delay(orm_created_file.pk)

        return default_result
    

class FilesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer