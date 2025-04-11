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

"""Client for managing received Electronic Fee Receipts (BHE)."""
from urllib.parse import urlencode

from .. import ApiBase


class Bhe(ApiBase):

    """
    Module for managing received Electronic Fee Receipts (BHE).

    Provides methods for listing, retrieving, observing, and downloading
    received BHEs.

    :param api_token: User authentication token. If not provided, it will
                    be retrieved from an environment variable.
    :type api_token: str

    :param api_url: Base URL of the API. If not provided, a default
                    URL will be used.
    :type api_url: str

    :param api_version: API version to use. If not specified, the default
                        version will be used.
    :type api_version: str

    :param api_raise_for_status: Whether to raise an exception automatically
                                for HTTP error responses (default: True).
    :type api_raise_for_status: bool
    """

    def __init__(self):
        """
        Initialize the Bhe client instance.

        Inherits all configuration parameters from the base class `ApiBase`,
        including authentication, API URL, and behavior on HTTP errors.
        """
        super().__init__()

    def listar(self, filtros = None):
        """
        List received Electronic Fee Receipts (BHEs) with optional filters.

        Fetches a paginated list of received BHEs based on the given filters.

        :param filtros: Optional filters to apply to the query.
        :type filtros: dict

        :return: JSON response containing the list of received BHEs.
        :rtype: dict
        """
        if filtros is None:
            filtros = {}

        url = '/bhe/boletas'
        if filtros:
            query_string = urlencode(filtros)
            url += '?%(query)s' % {'query': query_string}

        response = self.client.get(url)

        return response.json()

    def datos(self, emisor, numero):
        """
        Retrieve the details of a specific received BHE.

        :param emisor: RUT of the BHE issuer (without dots, includes DV).
        :type emisor: str

        :param numero: BHE document number.
        :type numero: int

        :return: JSON response containing the BHE data.
        :rtype: dict
        """
        url = '/bhe/boletas/%(emisor)s/%(numero)s' % {
            'emisor': emisor, 'numero': numero
        }

        response = self.client.get(url)

        return response.json()

    def pdf(self, emisor, numero, filtros = None):
        """
        Download the PDF of a specific received BHE.

        :param emisor: RUT of the BHE issuer (without dots, includes DV).
        :type emisor: str

        :param numero: BHE document number.
        :type numero: int

        :param filtros: Optional filters (e.g., options for download format).
        :type filtros: dict

        :return: PDF file as a byte stream.
        :rtype: bytes
        """
        if filtros is None:
            filtros = {}

        url = '/bhe/pdf/%(emisor)s/%(numero)s' % {
            'emisor': emisor, 'numero': numero
        }

        if filtros:
            query_string = urlencode(filtros)
            url += '?%(query)s' % {'query': query_string}

        response = self.client.get(url)

        return response.content

    def observar(self, emisor, numero, body):
        """
        Submit an observation to a previously received BHE.

        :param emisor: RUT of the BHE issuer (without dots, includes DV).
        :type emisor: str

        :param numero: BHE document number.
        :type numero: int

        :param body: Dictionary containing the observation data (e.g., reason).
        :type body: dict

        :return: JSON response with the updated BHE status.
        :rtype: dict
        """
        url = '/bhe/observar/%(emisor)s/%(numero)s' % {
            'emisor': emisor, 'numero': numero
        }

        response = self.client.post(url, body)

        return response.json()

    def listar_emisores(self, nuevos):
        """
        List all BHE issuers, optionally filtering by newly added ones.

        :param nuevos: Indicates if only issuers who sent a BHE for the first
                    time in the period should be returned.
        :type nuevos: str

        :return: JSON response containing the list of issuers.
        :rtype: dict
        """
        url = '/bhe/emisores?nuevos=%(nuevos)s' % {
            'nuevos': nuevos
        }

        response = self.client.get(url)

        return response.json()
