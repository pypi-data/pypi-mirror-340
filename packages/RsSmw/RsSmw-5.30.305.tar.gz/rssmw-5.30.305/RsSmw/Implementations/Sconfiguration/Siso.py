from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SisoCls:
	"""Siso commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("siso", core, parent)

	# noinspection PyTypeChecker
	def get_route(self) -> enums.PathFaderOut:
		"""SCPI: SCONfiguration:SISO:ROUTe \n
		Snippet: value: enums.PathFaderOut = driver.sconfiguration.siso.get_route() \n
		No command help available \n
			:return: routing_siso: No help available
		"""
		response = self._core.io.query_str('SCONfiguration:SISO:ROUTe?')
		return Conversions.str_to_scalar_enum(response, enums.PathFaderOut)

	def set_route(self, routing_siso: enums.PathFaderOut) -> None:
		"""SCPI: SCONfiguration:SISO:ROUTe \n
		Snippet: driver.sconfiguration.siso.set_route(routing_siso = enums.PathFaderOut.FAABFBA) \n
		No command help available \n
			:param routing_siso: No help available
		"""
		param = Conversions.enum_scalar_to_str(routing_siso, enums.PathFaderOut)
		self._core.io.write(f'SCONfiguration:SISO:ROUTe {param}')
