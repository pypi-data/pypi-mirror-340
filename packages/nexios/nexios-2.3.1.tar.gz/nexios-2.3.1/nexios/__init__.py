"""
Implemented based on Starlette version 0.45.3.

This module adapts selected components and logic from Starlette to ensure compatibility
with our internal architecture, while preserving the async-first design principles and
middleware patterns that Starlette is known for.

Key inspirations from Starlette include:
- ASGI application structure
- Middleware handling pattern


Note: Adjustments have been made for dependency injection, custom error handling,
and simplified routing mechanisms to better suit the Nexios framework architecture.
"""

from .application import NexiosApp
from .sessions.middleware import SessionMiddleware
from .middlewares.csrf import CSRFMiddleware
from .config.base import MakeConfig
from .config import set_config, DEFAULT_CONFIG
from .routing import Router  # type:ignore
from .middlewares.cors import CORSMiddleware
from typing import Optional, Callable, AsyncIterator
from .application import NexiosApp
from .types import ExceptionHandlerType
from typing_extensions import Doc, Annotated
from nexios.middlewares.core import wrap_middleware


def get_application(
    config: Annotated[
        MakeConfig,
        Doc(
            """
                    This subclass is derived from the MakeConfig class and is responsible for managing configurations within the Nexios framework. It takes arguments in the form of dictionaries, allowing for structured and flexible configuration handling. By using dictionaries, this subclass makes it easy to pass multiple configuration values at once, reducing complexity and improving maintainability.

                    One of the key advantages of this approach is its ability to dynamically update and modify settings without requiring changes to the core codebase. This is particularly useful in environments where configurations need to be frequently adjusted, such as database settings, API credentials, or feature flags. The subclass can also validate the provided configuration data, ensuring that incorrect or missing values are handled properly.

                    Additionally, this design allows for merging and overriding configurations, making it adaptable for various use cases. Whether used for small projects or large-scale applications, this subclass ensures that configuration management remains efficient and scalable. By extending MakeConfig, it leverages existing functionality while adding new capabilities tailored to Nexios. This makes it an essential component for maintaining structured and well-organized application settings.
                    """
        ),
    ] = DEFAULT_CONFIG,
    server_error_handler: Annotated[
        Optional[ExceptionHandlerType],
        Doc(
            """
                        A function in Nexios responsible for handling server-side exceptions by logging errors, reporting issues, or initiating recovery mechanisms. It prevents crashes by intercepting unexpected failures, ensuring the application remains stable and operational. This function provides a structured approach to error management, allowing developers to define custom handling strategies such as retrying failed requests, sending alerts, or gracefully degrading functionality. By centralizing error processing, it improves maintainability and observability, making debugging and monitoring more efficient. Additionally, it ensures that critical failures do not disrupt the entire system, allowing services to continue running while appropriately managing faults and failures."""
        ),
    ] = None,
    lifespan: Optional[Callable[["NexiosApp"], AsyncIterator[None]]] = None,
) -> NexiosApp:
    """
    Initializes and returns a `Nexios` application instance, serving as the core entry point for building web applications.

    Nexios is a lightweight, asynchronous Python framework designed for speed, flexibility, and ease of use.
    This function sets up the necessary configurations and routing mechanisms, allowing developers
    to define routes, handle requests, and manage responses efficiently.

    ## Example Usage

    ```python
    from nexios import Nexios
    config = MakeConfig({
        "debug" : True
    })
    app = get_application(config = config)
    ```

    Returns:
        Nexios: An instance of the Nexios application, ready to register routes and handle requests.

    See Also:
        - [Nexios Documentation](https://example.com/nexios-docs)
    """

    set_config(config)
    app = NexiosApp(
        middlewares=[
            wrap_middleware(CORSMiddleware()),
            wrap_middleware(SessionMiddleware()),
            wrap_middleware(CSRFMiddleware()),
        ],
        server_error_handler=server_error_handler,  # type:ignore
        config=config,
        lifespan=lifespan,
    )

    return app


__all__ = ["MakeConfig", "Router"]
