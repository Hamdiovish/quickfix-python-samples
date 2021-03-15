def get_header_value(message, field):
    """
    :param message: fix.Message()
    :param field: fix.FieldBase()
    :return: Value of the given field key
    """

    return get_field_value(message.getHeader(), field)


def get_field_value(message, field):
    """
    :param message: fix.Message() or fix.Header() or fix.Group()
    :param field: fix.FieldBase()
    :return: Value of the given field key
    """
    if message.isSetField(field):
        message.getField(field)
        return field.getValue()
    raise ValueError("Trying to access an unset field", field)


def parse_message(message):
    return message.toString().replace(chr(1), "|")
