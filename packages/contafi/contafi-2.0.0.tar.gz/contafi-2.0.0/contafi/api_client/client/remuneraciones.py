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

"""Client for retrieving information related to employee payroll."""
from .. import ApiBase


class Remuneraciones(ApiBase):

    """
    Module for retrieving information related to employee payroll.

    This class provides access to salary records (remuneraciones) for a
    taxpayer, including optional filtering by period.

    :param api_token: User authentication token. If not provided, it will
                    be read from an environment variable.
    :type api_token: str

    :param api_url: Base API URL. If not provided, a default will be used.
    :type api_url: str

    :param api_version: API version. If not specified, a default version
                        will be used.
    :type api_version: str

    :param api_raise_for_status: Whether to raise an exception on HTTP error
                                responses. Defaults to True.
    :type api_raise_for_status: bool
    """

    def __init__(self):
        """
        Initialize the Remuneraciones client instance.

        Inherits API configuration from the `ApiBase` class.
        """
        super().__init__()

    def listar_remuneraciones(self, periodo = None):
        """
        Retrieve a paginated list of remuneration records for the taxpayer.

        :param periodo: Optional period to filter the payroll list.
        :type periodo: str

        :return: JSON response containing the remuneration records.
        :rtype: dict
        """
        url = '/remuneraciones'

        if periodo is not None:
            url += '?periodo=%(periodo)s' % {'periodo': periodo}

        response = self.client.get(url)

        return response.json()
