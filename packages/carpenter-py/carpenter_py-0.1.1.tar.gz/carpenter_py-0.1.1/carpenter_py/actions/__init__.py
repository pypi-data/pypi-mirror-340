from functools import wraps
import inspect
import os
import json
import importlib
import traceback
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse
from typing import Callable, Awaitable, Optional, Any, Type
from typing import get_type_hints
from pydantic import BaseModel
from carpenter_py.utils.log import logger

action_registry = {}
action_metadata = {}


def action(model: Optional[Type[BaseModel]] = None):
    def decorator(
        fn: Callable[..., Awaitable[Any]],
    ) -> Callable[[Request], Awaitable[JSONResponse]]:
        @wraps(fn)
        async def wrapper(request: Request) -> JSONResponse:
            try:
                validated = None
                if model:
                    body = await request.json()
                    validated = model(**body)
                    result = await fn(validated, request)
                else:
                    result = await fn(request)

                if isinstance(result, BaseModel):
                    result = result.model_dump()

                if isinstance(result, dict) and "status" in result:
                    return JSONResponse(content=result)

                return JSONResponse(content={"status": "success", "result": result})

            except Exception as e:
                logger.error(f"[ACTION ERROR] Exception in '{fn.__name__}': {e}")
                logger.debug(traceback.format_exc())
                return JSONResponse(
                    {
                        "status": "error",
                        "error": str(e),
                        "details": "Error while processing action",
                    },
                    status_code=500,
                )

        try:
            module = inspect.getmodule(fn)
            if not module:
                raise ValueError("Could not determine module for function")

            route_base = (
                module.__name__.replace("pages.", "")
                .replace(".server", "")
                .replace(".actions", "")
            )
            route_path = f"{route_base}/{fn.__name__}".strip("/")

            input_type = model.__name__ if model else "None"
            output_type = "JSONResponse"

            action_metadata[route_path] = {
                "input": input_type,
                "output": output_type,
            }

            action_registry[route_path] = wrapper
        except Exception as e:
            logger.error(
                f"[ACTION ERROR] Failed to register action '{fn.__name__}': {e}"
            )
            logger.debug(traceback.format_exc())

        return wrapper

    return decorator


def generate_action_type_map() -> dict:
    """
    Generates the action type map, including the fields for input and output models.
    """
    return {
        path: {
            "input": {
                "type": metadata["input"],
                "fields": metadata.get("input_fields", {}),
            },
            "output": {
                "type": metadata["output"],
                "fields": metadata.get("output_fields", {}),
            },
        }
        for path, metadata in action_metadata.items()
    }


def export_action_type_map():
    """
    Exports the action type map to a JSON file, including fields for input and output.
    Uses reflection to extract model fields just like `get_action_docs`.
    """
    for route_path, handler in action_registry.items():
        fn = getattr(handler, "__wrapped__", handler)
        sig = inspect.signature(fn)
        type_hints = get_type_hints(fn)

        input_type_name = "None"
        input_type_fields = {}
        output_type_name = "None"
        output_type_fields = {}

        for name, _ in sig.parameters.items():
            if name == "request":
                continue

            annotation = type_hints.get(name)
            if (
                annotation
                and isinstance(annotation, type)
                and issubclass(annotation, BaseModel)
            ):
                input_type_name = annotation.__name__
                input_type_fields = extract_model_fields(annotation)
                break

        return_annotation = type_hints.get("return")
        if (
            return_annotation
            and isinstance(return_annotation, type)
            and issubclass(return_annotation, BaseModel)
        ):
            output_type_name = return_annotation.__name__
            output_type_fields = extract_model_fields(return_annotation)

        action_metadata[route_path]["input"] = input_type_name
        action_metadata[route_path]["input_fields"] = input_type_fields
        action_metadata[route_path]["output"] = output_type_name
        action_metadata[route_path]["output_fields"] = output_type_fields

    action_type_map = generate_action_type_map()

    with open("action_map.json", "w") as f:
        json.dump(action_type_map, f, indent=2)


def get_action_routes() -> list[Route]:
    routes = []
    for path, fn in action_registry.items():

        async def endpoint(request: Request, fn=fn):
            try:
                result = await fn(request)
                if isinstance(result, BaseModel):
                    result = result.model_dump()
                    return JSONResponse(result)
                if isinstance(result, JSONResponse):
                    return result
                return JSONResponse(content=result)
            except Exception as e:
                logger.error(f"[ACTION ERROR] Exception in endpoint '{path}': {e}")
                logger.debug(traceback.format_exc())
                return JSONResponse(
                    {"error": str(e), "details": f"Error in action endpoint: {path}"},
                    status_code=500,
                )

        routes.append(Route(f"/_actions/{path}", endpoint, methods=["POST"]))
    return routes


def import_page_actions():
    for root, _, files in os.walk("pages"):
        for name in ("server.py", "actions.py"):
            if name in files:
                rel_path = os.path.relpath(os.path.join(root, name)).replace(
                    os.sep, "."
                )
                module_path = rel_path.replace(".py", "")
                try:
                    importlib.import_module(module_path)
                except Exception as e:
                    logger.error(f"[ACTIONS ERROR] Failed to import {module_path}: {e}")
                    logger.debug(traceback.format_exc())


def get_action_metadata():
    try:
        return [
            {"path": f"/_actions/{path}", "name": fn.__name__}
            for path, fn in action_registry.items()
        ]
    except Exception as e:
        logger.error(f"[ACTIONS ERROR] Failed to get metadata: {e}")
        logger.debug(traceback.format_exc())
        return []


def extract_model_fields(model_cls):
    return {
        name: (field.__name__ if hasattr(field, "__name__") else str(field))
        for name, field in model_cls.__annotations__.items()
    }


def get_action_docs():
    """
    Generates documentation and extracts input/output fields.
    """
    docs = []

    for route_path, handler in action_registry.items():
        fn = getattr(handler, "__wrapped__", handler)
        sig = inspect.signature(fn)
        type_hints = get_type_hints(fn)

        params = {}
        input_type_name = "Record<string, any>"
        input_type_fields = None

        for name, _ in sig.parameters.items():
            if name == "self":
                continue

            annotation = type_hints.get(name, str)

            if isinstance(annotation, type) and issubclass(annotation, BaseModel):
                input_type_name = annotation.__name__
                input_type_fields = extract_model_fields(annotation)

            params[name] = (
                annotation.__name__
                if hasattr(annotation, "__name__")
                else str(annotation)
            )
            params[f"{name}_fields"] = extract_model_fields(annotation)

        return_annotation = type_hints.get("return", None)

        if return_annotation is None or return_annotation is type(None):
            return_type_name = "None"
            output_type_fields = None
        elif isinstance(return_annotation, type) and issubclass(
            return_annotation, BaseModel
        ):
            return_type_name = return_annotation.__name__
            output_type_fields = extract_model_fields(return_annotation)
        else:
            return_type_name = (
                return_annotation.__name__
                if hasattr(return_annotation, "__name__")
                else str(return_annotation)
            )
            output_type_fields = None

        docs.append(
            {
                "name": fn.__name__,
                "path": f"/_actions/{route_path}",
                "method": getattr(handler, "method", "POST"),
                "params": params,
                "doc": fn.__doc__.strip() if fn.__doc__ else "",
                "input_type": input_type_name,
                "input_fields": input_type_fields,
                "output_type": return_type_name,
                "output_fields": output_type_fields,
            }
        )

    return docs
