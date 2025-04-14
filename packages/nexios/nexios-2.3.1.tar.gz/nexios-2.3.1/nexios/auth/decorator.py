from nexios.decorators import RouteDecorator
import typing
from .exceptions import AuthenticationFailed
from nexios.http import Request, Response


class auth(RouteDecorator):

    def __init__(self, scopes: typing.Union[str, typing.List[str], None] = None):
        super().__init__()
        if isinstance(scopes, str):
            self.scopes = [scopes]
        elif scopes is None:
            self.scopes = []  # Allow authentication with any scope
        else:
            self.scopes = scopes

    def __call__(
        self, handler: typing.Callable[..., typing.Awaitable[typing.Any]]
    ) -> typing.Any:
        async def wrapper(
            *args: typing.List[typing.Any], **kwargs: typing.Dict[str, typing.Any]
        ) -> typing.Any:
            *_, request, response = args  # Ensure request and response are last

            if not isinstance(request, Request) or not isinstance(response, Response):
                raise TypeError("Expected request and response as the last arguments")

            if not request.scope.get("user"):
                raise AuthenticationFailed

            scope = request.scope.get("auth")  # type: ignore

            if self.scopes and scope not in self.scopes:
                raise AuthenticationFailed

            return await handler(request, response)

        return wrapper
