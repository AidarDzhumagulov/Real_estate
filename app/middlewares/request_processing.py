from functools import partial
from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute
from starlette.background import BackgroundTask, BackgroundTasks


class RequestProcessingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        handler = super().get_route_handler()

        return partial(self.custom_route_handler, handler=handler)

    @classmethod
    async def custom_route_handler(cls, request: Request, handler) -> Response:
        response = await handler(request)
        if request.method == "OPTIONS":
            return response

        if request.headers.get("Content-Type") == "application/json":
            await request.json()

        if response.background is None:
            response.background = BackgroundTasks()
        elif isinstance(response.background, BackgroundTask):
            task = response.background
            response.background = BackgroundTasks()
            response.background.add_task(task)

        return response
