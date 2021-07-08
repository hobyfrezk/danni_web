from rest_framework.response import Response


def serializer_error_response(serializer):
    return Response({
        'success': False,
        'message': 'Please check input.',
        'errors': serializer.errors,
    }, status=400)