from starlette.requests import Request
from starlette.responses import Response


def request_key_builder(
        func,
        namespace: str = '',
        request: Request = None,
        response: Response = None,
        *args,
        **kwargs,
) -> str:
    return ':'.join([
        request.url.path,
    ])
