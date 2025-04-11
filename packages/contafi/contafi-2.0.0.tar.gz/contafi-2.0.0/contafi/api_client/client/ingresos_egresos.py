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

"""Client for managing and listing monetary transactions (income/expenses)."""
from .. import ApiBase


class IngresosEgresos(ApiBase):

    """
    Module for managing and listing monetary transactions (income/expenses).

    This class provides access to the list of money movements performed
    or received by the taxpayer for a given period.

    :param api_token: User authentication token. If not provided, it will
                    be retrieved from an environment variable.
    :type api_token: str

    :param api_url: Base API URL. If not provided, a default will be used.
    :type api_url: str

    :param api_version: API version. If not provided, a default version
                        will be used.
    :type api_version: str

    :param api_raise_for_status: Whether to raise an exception automatically
                                on HTTP error responses. Defaults to True.
    :type api_raise_for_status: bool
    """

    def __init__(self):
        """
        Initialize the IngresosEgresos client instance.

        Inherits configuration and HTTP behavior from the `ApiBase` class.
        """
        super().__init__()

    def listar_movimientos(self, periodo):
        """
        Retrieve a paginated list of income/expense transactions for a period.

        :param periodo: Period for which to retrieve the list of transactions.
        :type periodo: str

        :return: JSON response with all performed and received movements.
        :rtype: dict
        """
        url = '/movimientos?periodo=%(periodo)s' % {'periodo': periodo}

        response = self.client.get(url)

        return response.json()
