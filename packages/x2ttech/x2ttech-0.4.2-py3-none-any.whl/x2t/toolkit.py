import base64
from functools import wraps
import io
import os
import platform
import re
import sys
import json
import hmac
import hashlib
import time
import requests
import unidecode

from PIL import Image as PILImage
from datetime import datetime
from typing import Any, Callable, Dict, Optional, Tuple
from threading import Thread
from urllib.parse import urlencode
from requests import Response, get, post, put, patch, delete
from pathlib import Path


class Toolkit:
    """A consolidated toolkit class with static utility methods."""

    def __init__(self, logger):
        """Initialize the Toolkit class with a logger instance."""
        self.logger = logger

    def slugify(self, text: str) -> str:
        """Convert a string into a slug-friendly uppercase format."""
        text = unidecode.unidecode(text).upper()
        return re.sub(r'[^A-Z0-9]', '', text)

    def convert_url_to_base64(self, url: str) -> str | bool:
        """Convert image URL to base64 string."""
        try:
            return base64.b64encode(requests.get(url.strip()).content).replace(b"\n", b"").decode()
        except Exception as e:
            self.logger.exception("Error converting URL to base64: %s", str(e))
            return False

    def resize_image(self, source_base64: str, width: int, height: int, fmt: str = 'PNG') -> str:
        """
        Resize a base64-encoded image to the given dimensions and return the resized image as base64.
        """
        try:
            image_bytes = base64.b64decode(source_base64)
            with io.BytesIO(image_bytes) as input_buffer:
                image = PILImage.open(input_buffer)
                resized_image = image.resize((width, height))
                with io.BytesIO() as output_buffer:
                    resized_image.save(output_buffer, format=fmt)
                    return base64.b64encode(output_buffer.getvalue()).decode('utf-8')
        except (base64.binascii.Error, IOError) as e:
            self.logger.exception("Error resizing image: %s", str(e))
            raise ValueError("Invalid image data or processing error") from e
    
    def start_background_thread(self, api, res_ids, res_model, func_name, pool, uid, context):
        def _target():
            try:
                with pool.cursor() as cr:
                    env = api.Environment(cr, uid, context)
                    records = env[res_model].sudo().browse(res_ids)
                    if hasattr(records, func_name):
                        method = getattr(records, func_name)
                        if callable(method):
                            return method()
            except Exception as e:
                self.logger.exception(
                    "Error running %s in background thread: %s", func_name, str(e))
        Thread(target=_target, daemon=True).start()

    def sign(self, endpoint: str, params: Dict[str, Any], app_secret: str, body: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate an HMAC-SHA256 signature for OpenAPI request.
        """
        sorted_keys = sorted(key for key in params if key not in {
                             "sign", "access_token"})
        input_data = "".join(f"{key}{params[key]}" for key in sorted_keys)

        if body:
            body_encoded: str = json.dumps(body)
            input_data += body_encoded

        input_data = f"{app_secret}{endpoint}{input_data}{app_secret}"
        return hmac.new(app_secret.encode(), input_data.encode(), hashlib.sha256).hexdigest()

    def parameter(
        self,
        obj: Any,
        properties: Dict[str, str],
        content_type: str = "application/json"
    ) -> Tuple[Dict[str, str], Dict[str, str]]:
        """
        Generate headers and queries based on dynamic object properties,
        supporting nested attribute access like 'service_id.app_key'.
        """
        def get_nested_attr(obj: Any, attr_path: str):
            for attr in attr_path.split("."):
                obj = getattr(obj, attr, None)
                if obj is None:
                    return None
            return obj
        timestamp = str(int(datetime.timestamp(datetime.now())))
        headers = {"Content-Type": content_type}
        queries = {"timestamp": timestamp}
        for key, attr_path in properties.items():
            value = get_nested_attr(obj, attr_path)
            if value is not None:
                if key.startswith("header_"):
                    headers[key.replace("header_", "")] = value
                elif key.startswith("query_"):
                    queries[key.replace("query_", "")] = value

        return headers, queries

    def call(
        self,
        base_url: str,
        endpoint: str,
        method: Callable[..., Response],
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        body: Optional[Dict[str, Any]] = None,
    ) -> Response:
        """
        Make an API call to the specified endpoint using the provided method.
        """
        if method not in {get, post, put, patch, delete}:
            raise ValueError(
                "Invalid method. Must be one of: get, post, put, patch, delete.")

        params = params or {}
        params.setdefault("timestamp", str(
            int(datetime.timestamp(datetime.now()))))
        query_string = urlencode(params)
        url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}?{query_string}"
        return method(url=url, headers=headers, json=body)

    def catch(self, log: bool = True, timing: bool = False, callback: dict = {}):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.perf_counter() if timing else None
                this = args[0]
                try:
                    result = func(*args, **kwargs)
                    if timing:
                        elapsed_time = time.perf_counter() - start_time
                        self.logger.info(
                            f"function {func.__name__} with measured time is {elapsed_time}s.")
                    return result
                except Exception as e:
                    if log:
                        self.logger.exception(
                            f"An error occurred in {func.__name__}: {e}")
                    _model = callback.get('_model')
                    _func = callback.get('_func')
                    this = this.env[_model]
                    if _model and _func:
                        if hasattr(this, _func):
                            _method = getattr(this, _func)
                            if callable(_method):
                                return _method(message=e)
            return wrapper
        return decorator
