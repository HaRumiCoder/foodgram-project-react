from rest_framework import generics, mixins


class CreateDeleteAPIView(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
