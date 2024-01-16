from .models import Item
from django.http import FileResponse
from rest_framework import permissions

from .serializers import ItemSerializer
from rest_framework.generics import RetrieveUpdateAPIView
from neural_network import model_weights
from django.core.files.storage import default_storage
import base64


class ItemViewSet(RetrieveUpdateAPIView):
    queryset = Item.objects.all().order_by('id')
    serializer_class = ItemSerializer
    permission_classes = [permissions.AllowAny]
    neural_controller = model_weights.Controller()

    def post(self, request):
        file = request.FILES['file']
        file_name = default_storage.save(file.name, file)
        res = self.neural_controller.predict(file_name)
        with open('E:\\JobBACK\\backend\\neural_network\\Dataset\\tracks\\000002.mp3', 'rb') as f:
            file_data = base64.b64encode(f.read()).decode('utf-8')
        return FileResponse(file_data)
