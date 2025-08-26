class PorscheException(Exception):
    def __str__(self):
        return f"Porsche异常: {str(self.args[0])}"
