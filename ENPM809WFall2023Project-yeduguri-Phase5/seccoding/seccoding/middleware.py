# middleware.py

import logging
import time

logger = logging.getLogger('url_logger')


class UrlLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()

        elapsed_time = end_time - start_time

        logger.info(f"{request.method} {request.path} - Status: {response.status_code} - "
                    f"Elapsed Time: {elapsed_time:.2f}s")

        return response
