from rest_framework.exceptions import ParseError

def get_key_or_400(request, field):
    result = request.data.get(field)
    if not result:
        raise ParseError({f"{field}": ["This field is required"]})
    return result