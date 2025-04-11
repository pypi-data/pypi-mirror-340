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

"""Client for managing taxpayers, including roles and permissions."""
from .. import ApiBase


class Contribuyentes(ApiBase):

    """
    Module for managing taxpayers in ContaFi, including roles and permissions.

    Provides methods for querying taxpayer data, managing authorized users,
    and modifying role-based permissions.

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
        Initialize the Contribuyentes client instance.

        Inherits API-related configuration from the `ApiBase` class.
        """
        super().__init__()

    def estadisticas(self):
        """
        Retrieve statistics for the current taxpayer (based on RUT).

        :return: JSON response containing taxpayer statistics.
        :rtype: dict
        """
        url = '/contribuyentes/estadisticas'

        response = self.client.get(url)

        return response.json()

    def datos(self, rut):
        """
        Retrieve taxpayer information based on RUT.

        :param rut: Taxpayer's RUT (without dots, includes DV).
        :type rut: str

        :return: JSON response with taxpayer details.
        :rtype: dict
        """
        url = '/contribuyentes/%(rut)s' % {'rut': rut}

        response = self.client.get(url)

        return response.json()

    def sucursal(self, sucursal):
        """
        Retrieve information for a specific taxpayer branch office.

        :param sucursal: Branch office ID.
        :type sucursal: int

        :return: JSON response with branch data.
        :rtype: dict
        """
        url = '/contribuyentes/sucursales/%(sucursal)s' % {
            'sucursal': sucursal
        }

        response = self.client.get(url)

        return response.json()

    def agregar_usuario_autorizado(self, body):
        """
        Authorize a user for the taxpayer with a specific role.

        :param body: Dictionary containing username and role to assign.
        :type body: dict

        :return: JSON response with the authorized user information.
        :rtype: dict
        """
        url = '/contribuyentes/usuarios'

        response = self.client.put(url, body)

        return response.json()

    def quitar_usuario_autorizado(self, usuario, rol):
        """
        Remove an authorized user and role from the taxpayer.

        :param usuario: Username to be removed.
        :type usuario: str

        :param rol: Role ID assigned to the user.
        :type rol: int

        :return: JSON response with information of the removed user.
        :rtype: dict
        """
        url = '/contribuyentes/usuarios/%(usuario)s/%(rol)s' % {
            'usuario': usuario,
            'rol': rol
        }

        response = self.client.delete(url)

        return response.json()

    def obtener_roles(self):
        """
        Retrieve the list of roles available for the taxpayer.

        :return: JSON response with the role definitions.
        :rtype: dict
        """
        url = '/contribuyentes/roles'

        response = self.client.get(url)

        return response.json()

    def agregar_permiso_rol(self, body):
        """
        Add one or more permissions to a role.

        :param body: Dictionary with role ID and permissions to add.
        :type body: dict

        :return: JSON response with the updated role.
        :rtype: dict
        """
        url = '/contribuyentes/roles'

        response = self.client.put(url, body)

        return response.json()

    def quitar_permiso_rol(self, id_rol, permiso):
        """
        Remove a permission from a taxpayer's role.

        :param id_rol: Unique identifier of the role.
        :type id_rol: int

        :param permiso: Name of the permission to remove.
        :type permiso: str

        :return: JSON response with the updated role.
        :rtype: dict
        """
        url = '/contribuyentes/roles/%(rol)s/%(permiso)s' % {
            'rol': id_rol,
            'permiso': permiso
        }

        response = self.client.delete(url)

        return response.json()
