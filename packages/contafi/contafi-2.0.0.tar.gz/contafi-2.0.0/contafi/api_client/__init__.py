#
# ContaFi: Cliente de API en Python.
# Copyright (C) ContaFi <https://www.contafi.cl>
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la GNU Lesser General Public License (LGPL) publicada
# por la Fundación para el Software Libre, ya sea la versión 3 de la Licencia,
# o (a su elección) cualquier versión posterior de la misma.
#
# Este programa se distribuye con la esperanza de que sea útil, pero SIN
# GARANTÍA ALGUNA; ni siquiera la garantía implícita MERCANTIL o de APTITUD
# PARA UN PROPÓSITO DETERMINADO. Consulte los detalles de la GNU Lesser General
# Public License (LGPL) para obtener una información más detallada.
#
# Debería haber recibido una copia de la GNU Lesser General Public License
# (LGPL) junto a este programa. En caso contrario, consulte
# <http://www.gnu.org/licenses/lgpl.html>.
#

"""
ContaFi API client package.

Contains the core client logic and API base classes required to interact
with the ContaFi web services.
"""
import json
from os import getenv
from urllib.parse import urljoin

import requests


class ApiClient:

    """
    Client for interacting with the ContaFi API.

    Handles authentication, request headers, URL versioning, and
    request execution with error handling.

    :param token: User authentication token. If not provided, the value will be
                read from the environment variable `CONTAFI_API_TOKEN`.
    :type token: str

    :param url: Base URL of the API. Defaults to https://contafi.cl or
                the value of `CONTAFI_API_URL`.
    :type url: str

    :param version: API version. Defaults to 'v1'.
    :type version: str

    :param raise_for_status: Whether to raise exceptions on HTTP errors.
                            Defaults to True.
    :type raise_for_status: bool
    """

    __DEFAULT_URL = 'https://contafi.cl'
    __DEFAULT_VERSION = 'v1'

    def __init__(
            self,
            token = None,
            url = None,
            version = None,
            raise_for_status = True
        ):
        """
        Initialize the API client.

        Validates token, URL, and RUT, and prepares default request headers.
        """
        self.token = self.__validate_token(token)
        self.url = self.__validate_url(url)
        self.rut = self.__validate_rut()
        self.headers = self.__generate_headers()
        self.version = version or self.__DEFAULT_VERSION
        self.raise_for_status = raise_for_status

    def __validate_token(self, token):
        """
        Validate and return the authentication token.

        :param token: Token to validate or fallback to environment variable.
        :type token: str

        :return: Validated token.
        :rtype: str

        :raises ApiException: If the token is missing or invalid.
        """
        token = token or getenv('CONTAFI_API_TOKEN')
        if not token:
            raise ApiException(
                'Se debe configurar la variable de entorno: CONTAFI_API_TOKEN.'
            )
        return str(token).strip()

    def __validate_url(self, url):
        """
        Validate and return the API base URL.

        :param url: URL to validate.
        :type url: str

        :return: Validated URL string.
        :rtype: str

        :raises ApiException: If the URL is missing or invalid.
        """
        return str(url).strip() if url else getenv(
            'CONTAFI_API_URL', self.__DEFAULT_URL
        ).strip()

    def __validate_rut(self):
        """
        Validate and return the RUT of the taxpayer.

        :return: Validated taxpayer RUT.
        :rtype: str

        :raises ApiException: If the RUT is not set in the environment.
        """
        rut = getenv('CONTAFI_CONTRIBUYENTE_RUT', '')
        if rut == '':
            raise ApiException(
                'Se debe configurar la variable de entorno: '
                'CONTAFI_CONTRIBUYENTE_RUT.'
            )
        return str(rut).strip()

    def __generate_headers(self):
        """
        Generate default HTTP headers used in all API requests.

        :return: Dictionary with base headers.
        :rtype: dict
        """
        return {
            'User-Agent': 'ContaFi: Cliente de API en Python.',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Token %(token)s' % {'token': self.token},
            'X-Contafi-Contribuyente': self.rut
        }

    def get(self, resource, headers = None):
        """
        Send a GET request to the specified API resource.

        :param resource: API resource path (e.g., "/dte/ventas").
        :type resource: str

        :param headers: Optional custom headers.
        :type headers: dict

        :return: HTTP response object.
        :rtype: requests.Response
        """
        return self.__request('GET', resource, headers = headers)

    def delete(self, resource, headers = None):
        """
        Send a DELETE request to the specified API resource.

        :param resource: API resource path.
        :type resource: str

        :param headers: Optional custom headers.
        :type headers: dict

        :return: HTTP response object.
        :rtype: requests.Response
        """
        return self.__request('DELETE', resource, headers = headers)

    def post(self, resource, data = None, headers = None):
        """
        Send a POST request to the specified API resource.

        :param resource: API resource path.
        :type resource: str

        :param data: Data to send in the request body.
        :type data: dict

        :param headers: Optional custom headers.
        :type headers: dict

        :return: HTTP response object.
        :rtype: requests.Response
        """
        return self.__request(
            'POST',
            resource,
            data = data,
            headers = headers
        )

    def put(self, resource, data = None, headers = None):
        """
        Send a PUT request to the specified API resource.

        :param resource: API resource path.
        :type resource: str

        :param data: Data to send in the request body.
        :type data: dict

        :param headers: Optional custom headers.
        :type headers: dict

        :return: HTTP response object.
        :rtype: requests.Response
        """
        return self.__request(
            'PUT',
            resource,
            data = data,
            headers = headers
        )

    def __request(self, method, resource, data = None, headers = None):
        """
        Perform an HTTP request to the API.

        This internal method constructs the full URL, applies default headers,
        serializes the body if necessary, and returns the raw response.

        :param method: HTTP method (e.g., GET, POST).
        :type method: str

        :param resource: API resource path.
        :type resource: str

        :param data: Optional request body data.
        :type data: dict or str

        :param headers: Optional headers to include.
        :type headers: dict

        :return: HTTP response object.
        :rtype: requests.Response

        :raises ApiException: On connection, timeout, or request error.
        """
        api_path = '/api/%(version)s%(resource)s' % {
            'version': self.version, 'resource': resource
        }
        full_url = urljoin(
            self.url + '/', api_path.lstrip('/')
        )
        headers = headers or {}
        headers = {**self.headers, **headers}
        if data and not isinstance(data, str):
            data = json.dumps(data)
        try:
            response = requests.request(
                method, full_url, data = data, headers = headers
            )
            return self.__check_and_return_response(response)
        except requests.exceptions.ConnectionError as error:
            raise ApiException(
                'Error de conexión: %(error)s' % {'error': error}
            )
        except requests.exceptions.Timeout as error:
            raise ApiException(
                'Error de timeout: %(error)s' % {'error': error}
            )
        except requests.exceptions.RequestException as error:
            raise ApiException(
                'Error en la solicitud: %(error)s' % {'error': error}
            )

    def __check_and_return_response(self, response):
        """
        Validate an HTTP response and raise a standardized error if needed.

        :param response: HTTP response from the API.
        :type response: requests.Response

        :return: The validated response.
        :rtype: requests.Response

        :raises ApiException: If the status code is not 200 and
        raise_for_status is True.
        """
        status_success = 200
        if response.status_code != status_success and self.raise_for_status:
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                try:
                    error = response.json()
                    message = error.get(
                        'message', ''
                    ) or error.get(
                        'exception', ''
                    ) or error.get(
                        'detail', ''
                    ) or 'Error desconocido.'
                except json.decoder.JSONDecodeError:
                    message = 'Error al decodificar los datos en JSON: '
                    message += '%(response)s' % {
                        'response': response.reason
                    }
                raise ApiException('%(message)s (%(code)s)' % {
                    'message': message,
                    'code': response.status_code
                })
        return response

class ApiException(Exception):

    """
    Custom exception for handling errors in the ContaFi API client.

    This exception is raised when an HTTP error, connection failure,
    timeout, or malformed response occurs. It allows for an optional
    error code and additional contextual parameters.
    """

    def __init__(self, message, code = None, params = None):
        """
        Initialize the API exception.

        :param message: Error message describing the issue.
        :type message: str

        :param code: Optional error code (HTTP or application-specific).
        :type code: int, optional

        :param params: Optional dictionary with additional context or metadata.
        :type params: dict, optional
        """
        self.message = message
        self.code = code
        self.params = params
        super().__init__(message)

    def __str__(self):
        """
        Return a formatted string representation of the exception.

        The string includes the prefix "[ContaFi]" and optionally the
        error code if provided.

        Examples:
            "[ContaFi] Error 401: Invalid token"
            "[ContaFi] Unexpected error occurred."

        :return: A string describing the error.
        :rtype: str

        """
        if self.code is not None:
            return '[ContaFi] Error %(code)s: %(message)s' % {
                'code': self.code, 'message': self.message
            }
        else:
            return '[ContaFi] %(message)s' % {'message': self.message}

class ApiBase:

    """
    Abstract base class for ContaFi API wrappers.

    Used as a foundation for specialized modules that interact with
    specific API endpoints (e.g., BHE, BTE, invoices, etc.). Provides
    a preconfigured `ApiClient` instance to be reused by subclasses.

    :param api_token: Authentication token for the ContaFi API.
    :type api_token: str

    :param api_url: Base URL for the ContaFi API.
    :type api_url: str

    :param api_version: API version to use (e.g., "v1").
    :type api_version: str

    :param api_raise_for_status: Whether to raise an exception automatically
                                on HTTP error responses. Defaults to True.
    :type api_raise_for_status: bool
    """

    def __init__(
            self,
            api_token = None,
            api_url = None,
            api_version = None,
            api_raise_for_status = True
        ):
        """
        Initialize the base API wrapper and create a configured ApiClient.

        This client will be used by subclasses to perform HTTP operations
        with the appropriate authentication and configuration settings.

        :param api_token: API token for authorization.
        :type api_token: str

        :param api_url: Base API endpoint.
        :type api_url: str

        :param api_version: Version of the API to use.
        :type api_version: str

        :param api_raise_for_status: Enable automatic HTTP error raising.
        :type api_raise_for_status: bool
        """
        self.client = ApiClient(
            api_token,
            api_url,
            api_version,
            api_raise_for_status
        )
