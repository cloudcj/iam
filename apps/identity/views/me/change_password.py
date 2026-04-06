from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers, status

from apps.authn.tokens.service import issue_user_tokens
from apps.authn.tokens.cookies import set_auth_cookies


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
    confirm_password = serializers.CharField()

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    bypass_must_change_password = True

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = request.user
        if not user.check_password(data["current_password"]):
            return Response(
                {"current_password": ["Incorrect password."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(data["new_password"])
        user.must_change_password = False
        user.save(update_fields=["password", "must_change_password"])

        # Re-issue fresh tokens with updated must_change_password flag
        tokens = issue_user_tokens(user=user)

        response = Response({"detail": "Password changed successfully."})
        set_auth_cookies(response, access=tokens["access"], refresh=tokens["refresh"])
        return response
