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

"""Client for managing issued Third-Party Electronic Receipts (BTEs)."""
from urllib.parse import urlencode

from .. import ApiBase


class Bte(ApiBase):

    """
    Module for managing issued Third-Party Electronic Receipts (BTEs).

    This class provides methods for issuing, retrieving, canceling, and
    calculating BTEs, as well as listing related receivers.

    :param api_token: User authentication token. If not provided, it will
                    be read from an environment variable.
    :type api_token: str

    :param api_url: Base API URL. If not provided, a default will be used.
    :type api_url: str

    :param api_version: API version. If not provided, a default version
                        will be used.
    :type api_version: str

    :param api_raise_for_status: Whether to raise an exception on HTTP error
                                responses. Defaults to True.
    :type api_raise_for_status: bool
    """

    def __init__(self):
        """
        Initialize the Bte client instance.

        Inherits all configuration parameters from the `ApiBase` class,
        including authentication, API URL, and HTTP error handling.
        """
        super().__init__()

    def emitir(self, body):
        """
        Issue a new BTE.

        :param body: Dictionary containing the BTE data to be issued.
        :type body: dict

        :return: JSON response with the issued BTE.
        :rtype: dict
        """
        url = '/bte/emitir'

        response = self.client.post(url, body)

        return response.json()

    def listar(self, filtros = None):
        """
        Retrieve a paginated list of issued BTEs.

        :param filtros: Optional filters to apply (e.g., by period, RUT).
        :type filtros: dict

        :return: JSON response containing the list of issued BTEs.
        :rtype: dict
        """
        if filtros is None:
            filtros = {}

        url = '/bte/boletas'

        if filtros:
            query_string = urlencode(filtros)
            url += '?%(query)s' % {'query': query_string}

        response = self.client.get(url)

        return response.json()

    def datos(self, numero):
        """
        Retrieve the data of a specific issued BTE.

        :param numero: BTE document number.
        :type numero: int

        :return: JSON response with the BTE data.
        :rtype: dict
        """
        url = '/bte/boletas/%(numero)s' % {'numero': numero}

        response = self.client.get(url)

        return response.json()

    def html(self, numero):
        """
        Retrieve the HTML representation of a specific BTE.

        :param numero: BTE document number.
        :type numero: int

        :return: HTML content of the BTE as bytes.
        :rtype: bytes
        """
        url = '/bte/html/%(numero)s' % {'numero': numero}

        response = self.client.get(url)

        return response.content

    def pdf(self, numero):
        """
        Retrieve the PDF file of a specific BTE.

        :param numero: BTE document number.
        :type numero: int

        :return: PDF file of the BTE as bytes.
        :rtype: bytes
        """
        url = '/bte/pdf/%(numero)s' % {'numero': numero}

        response = self.client.get(url)

        return response.content

    def anular(self, numero, body):
        """
        Cancel a previously issued BTE.

        :param numero: BTE document number to cancel.
        :type numero: int

        :param body: Dictionary containing cancellation data (e.g., reason).
        :type body: dict

        :return: JSON response with the canceled BTE data.
        :rtype: dict
        """
        url = '/bte/anular/%(numero)s' % {'numero': numero}

        response = self.client.post(url, body)

        return response.json()

    def calcular_monto_liquido(self, bruto, periodo):
        """
        Calculate the net amount (monto líquido) from a gross amount.

        :param bruto: Gross amount to convert.
        :type bruto: int

        :param periodo: Period used for the conversion.
        :type periodo: str

        :return: JSON response with the calculated net value.
        :rtype: dict
        """
        url = '/bte/liquido/%(bruto)s/%(periodo)s' % {
            'bruto': bruto,
            'periodo': periodo
        }

        response = self.client.get(url)

        return response.json()

    def calcular_monto_bruto(self, liquido, periodo):
        """
        Calculate the gross amount (monto bruto) from a net amount.

        :param liquido: Net amount to convert.
        :type liquido: int

        :param periodo: Period used for the conversion.
        :type periodo: str

        :return: JSON response with the calculated gross value.
        :rtype: dict
        """
        url = '/bte/bruto/%(liquido)s/%(periodo)s' % {
            'liquido': liquido,
            'periodo': periodo
        }

        response = self.client.get(url)

        return response.json()

    def listar_receptores(self):
        """
        List all receivers associated with issued BTEs.

        :return: JSON response containing receiver information.
        :rtype: dict
        """
        url = '/bte/receptores'

        response = self.client.get(url)

        return response.json()
