from rest_framework_simplejwt.authentication import JWTAuthentication

class NoBearerJWTAuthentication(JWTAuthentication):
    def get_header(self, request):
        header = super().get_header(request)
        if header is None:
            return None
        return header.decode("utf-8").replace("Bearer ", "").encode("utf-8")
