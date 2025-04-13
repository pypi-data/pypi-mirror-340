from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from typing import Callable

VITE_ORIGIN = "http://localhost:3000"

class AuthorizationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            if request.url.path.startswith("/_actions"):
                origin = request.headers.get("origin")
                vite_header = request.headers.get("x-powered-by")

                if origin != VITE_ORIGIN and vite_header != "CarpenterJS":
                    return JSONResponse({"error": "Unauthorized"}, status_code=401)

            return await call_next(request)

        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
