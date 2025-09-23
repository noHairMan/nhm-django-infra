class PorscheException(Exception):
    default_detail = "An error occurred."

    def __init__(self, detail=None):
        if detail is None:
            detail = self.default_detail

        self.detail = detail

    def __str__(self):
        return str(self.detail)
