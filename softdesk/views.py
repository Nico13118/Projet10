from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from softdesk.models import User
from softdesk.permissions import IsUserAuthenticated, IsSuperUser
from softdesk.serializers import RegisterUserSerializer


# ModelViewSet : create()`, `retrieve()`, `update()`, `partial_update()`, `destroy()`, `list()`

class RegisterUserViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [AllowAny]

        else:
            self.permission_classes = [IsSuperUser]
        return super().get_permissions()


