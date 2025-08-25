from rest_framework.request import Request


class PorscheRequest(Request):
    @classmethod
    def from_request(cls, request: Request):
        return cls(
            request._request,
            parsers=request.parsers,
            authenticators=request.authenticators,
            negotiator=request.negotiator,
            parser_context=request.parser_context,
        )
