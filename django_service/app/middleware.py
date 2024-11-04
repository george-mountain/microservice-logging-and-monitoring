from django.utils.deprecation import MiddlewareMixin
from .metrics import request_counter
from .utils.logger_config import app_logger
from uuid import uuid4


class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        log_id = str(uuid4())
        with app_logger.contextualize(log_id=log_id):
            app_logger.info(f"Request to access {request.method} {request.path}")
            request_counter.labels(
                endpoint=request.path, method=request.method, status="in_progress"
            ).inc()

    def process_response(self, request, response):
        log_id = str(uuid4())
        with app_logger.contextualize(log_id=log_id):
            if response.status_code == 422:
                app_logger.error(
                    f"Unprocessable Entity: {request.method} {request.path}"
                )
                request_counter.labels(
                    endpoint=request.path, method=request.method, status="422"
                ).inc()
            else:
                app_logger.info(
                    f"Request to {request.method} {request.path} successful"
                )
                request_counter.labels(
                    endpoint=request.path,
                    method=request.method,
                    status=str(response.status_code),
                ).inc()
        return response

    def process_exception(self, request, exception):
        log_id = str(uuid4())
        with app_logger.contextualize(log_id=log_id):
            app_logger.error(
                f"Request to {request.method} {request.path} failed: {exception}"
            )
            request_counter.labels(
                endpoint=request.path, method=request.method, status="500"
            ).inc()
        return None
