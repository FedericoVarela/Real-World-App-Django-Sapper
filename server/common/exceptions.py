from rest_framework.exceptions import ParseError

def get_key_or_400(request, field):
    """ Utility for enforcing correct request shapes in views without serializers """
    result = request.data.get(field)
    if not result:
        raise ParseError({f"{field}": ["This field is required"]})
    return result