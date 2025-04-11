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

"""Client for managing suppliers, purchases, and sales using e-invoicing."""
from urllib.parse import urlencode

from .. import ApiBase


class Facturacion(ApiBase):

    """
    Module for managing suppliers, purchases, and sales using e-invoicing(DTE).

    This class provides methods for retrieving DTE records related to
    sales and purchases, as well as listing clients and suppliers.

    :param api_token: User authentication token. If not provided, it will
                    be read from an environment variable.
    :type api_token: str

    :param api_url: Base API URL. If not provided, a default will be used.
    :type api_url: str

    :param api_version: API version to use. If not specified, a default
                        version will be used.
    :type api_version: str

    :param api_raise_for_status: Whether to raise an exception on HTTP error
                                responses. Defaults to True.
    :type api_raise_for_status: bool
    """

    def __init__(self):
        """
        Initialize the Facturacion client instance.

        Inherits API-related configuration from the `ApiBase` class.
        """
        super().__init__()

    def resumen_ventas_sin_detalle(self, periodo):
        """
        Retrieve a paginated list of sales summaries for a given period.

        :param periodo: Period to filter the sales summary list (e.g.,2023-08).
        :type periodo: str

        :return: JSON response with the paginated list of sales summaries.
        :rtype: dict
        """
        url = '/dte/ventas/resumen?periodo=%(periodo)s' % {'periodo': periodo}

        response = self.client.get(url)

        return response.json()

    def listar_ventas(self, filtros = None):
        """
        Retrieve a paginated list of sales-related DTEs with full details.

        :param filtros: Optional filters to apply to the sales search.
        :type filtros: dict

        :return: JSON response containing the list of sales DTEs.
        :rtype: dict
        """
        if filtros is None:
            filtros = {}

        url = '/dte/ventas'

        if filtros:
            query_string = urlencode(filtros)
            url += '?%(query)s' % {'query': query_string}

        response = self.client.get(url)

        return response.json()

    def listar_compras(self, estado, filtros):
        """
        Retrieve a paginated list of purchase-related DTEs with full details.

        :param estado: Status of the document in the purchase register.
        :type estado: int

        :param filtros: Filters to apply to the query(e.g., by supplier, date).
        :type filtros: dict

        :return: JSON response with the paginated list of purchase DTEs.
        :rtype: dict
        """
        url = '/dte/compras?estado=%(estado)s' % {
            'estado': estado
        }

        if len(filtros) > 0:
            query_string = urlencode(filtros)
            url += '&%(query)s' % {'query': query_string}

        response = self.client.get(url)

        return response.json()

    def listar_clientes(self):
        """
        Retrieve a paginated list of clients associated with sales DTEs.

        :return: JSON response containing the list of sales clients.
        :rtype: dict
        """
        url = '/dte/clientes'

        response = self.client.get(url)

        return response.json()

    def listar_proveedores(self):
        """
        Retrieve a paginated list of suppliers associated with purchase DTEs.

        :return: JSON response containing the list of suppliers.
        :rtype: dict
        """
        url = '/dte/proveedores'

        response = self.client.get(url)

        return response.json()
