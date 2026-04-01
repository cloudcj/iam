# common/mixins.py
from rest_framework.response import Response
from rest_framework import status

class SuccessMessageMixin:
    create_message = "Created successfully."
    update_message = "Updated successfully."
    delete_message = "Deleted successfully."

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response(
            {
                "message": self.create_message,
                # "data": self.get_serializer(instance).data,
            },
            status=status.HTTP_201_CREATED,
        )

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response(
            {
                "message": self.update_message,
                # "data": self.get_serializer(instance).data,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response(
            {"message": self.delete_message},
            status=status.HTTP_200_OK,
            
        )
