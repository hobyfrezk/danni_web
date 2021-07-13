from rest_framework.response import Response
from decimal import Decimal


def serializer_error_response(serializer):
    return Response({
        'success': False,
        'message': 'Please check input.',
        'errors': serializer.errors,
    }, status=400)

def checkouts_error_response():
    return Response({
        'success': False,
        'message': 'Please check checkout type.',
    }, status=400)

def calculate_spending_amount(amount, pst, gst):
    # -(request.data["amount"] * (1 + request.data["pst"] + request.data["gst"]))
    convert = lambda x: Decimal(x).quantize(Decimal('.01'))
    amount = convert(amount)
    pst = convert(pst)
    gst = convert(gst)

    return - convert(amount + amount*pst + amount*gst)