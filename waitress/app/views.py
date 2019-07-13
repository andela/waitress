from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers


class SwaggerSchemaView(APIView):
    _ignore_model_permissions = False
    permission_classes = [AllowAny]
    exclude_from_schema = True
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer,
        renderers.JSONRenderer
    ]

    def get(self, request):
        generator = SchemaGenerator(title='Andela Waitress App')
        schema = generator.get_schema(request=request)

        return Response(schema)
