
class FourDigitYearConverter:
    # 1. regex
    regex = '[0-9]{4}'

    # 2. to_python
    def to_python(self, value):
        return int(value)

    # 3. to_url
    def to_url(self, value):
        return '%04d' % value
