from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RestartCls:
	"""Restart commands group definition. 4 total commands, 0 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("restart", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:RESTart \n
		Snippet: driver.source.cemulation.restart.set() \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:RESTart')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:RESTart \n
		Snippet: driver.source.cemulation.restart.set_with_opc() \n
		No command help available \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:CEMulation:RESTart', opc_timeout_ms)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.FadRestMode:
		"""SCPI: [SOURce<HW>]:CEMulation:RESTart:MODE \n
		Snippet: value: enums.FadRestMode = driver.source.cemulation.restart.get_mode() \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:RESTart:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FadRestMode)

	def set_mode(self, mode: enums.FadRestMode) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:RESTart:MODE \n
		Snippet: driver.source.cemulation.restart.set_mode(mode = enums.FadRestMode.AAUT) \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.FadRestMode)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:RESTart:MODE {param}')

	# noinspection PyTypeChecker
	def get_rmode(self) -> enums.TrigRunMode:
		"""SCPI: [SOURce<HW>]:CEMulation:RESTart:RMODE \n
		Snippet: value: enums.TrigRunMode = driver.source.cemulation.restart.get_rmode() \n
		No command help available \n
			:return: run_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:RESTart:RMODE?')
		return Conversions.str_to_scalar_enum(response, enums.TrigRunMode)

	# noinspection PyTypeChecker
	def get_source(self) -> enums.TrigSourRest:
		"""SCPI: [SOURce<HW>]:CEMulation:RESTart:SOURce \n
		Snippet: value: enums.TrigSourRest = driver.source.cemulation.restart.get_source() \n
		No command help available \n
			:return: rest_sour: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:RESTart:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.TrigSourRest)

	def set_source(self, rest_sour: enums.TrigSourRest) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:RESTart:SOURce \n
		Snippet: driver.source.cemulation.restart.set_source(rest_sour = enums.TrigSourRest.EGC1) \n
		No command help available \n
			:param rest_sour: No help available
		"""
		param = Conversions.enum_scalar_to_str(rest_sour, enums.TrigSourRest)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:RESTart:SOURce {param}')
