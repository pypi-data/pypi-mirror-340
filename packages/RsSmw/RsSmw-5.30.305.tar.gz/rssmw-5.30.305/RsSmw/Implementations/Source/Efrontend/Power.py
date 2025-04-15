from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PowerCls:
	"""Power commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("power", core, parent)

	def get_attenuation(self) -> float:
		"""SCPI: [SOURce<HW>]:EFRontend:POWer:ATTenuation \n
		Snippet: value: float = driver.source.efrontend.power.get_attenuation() \n
		Requires [SOURce<hw>]:EFRontend:AMODe MANual. Sets the attenuation of the external frontend. \n
			:return: attenuation: float Range: depends on connected device to depends on connected device
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:POWer:ATTenuation?')
		return Conversions.str_to_float(response)

	def set_attenuation(self, attenuation: float) -> None:
		"""SCPI: [SOURce<HW>]:EFRontend:POWer:ATTenuation \n
		Snippet: driver.source.efrontend.power.set_attenuation(attenuation = 1.0) \n
		Requires [SOURce<hw>]:EFRontend:AMODe MANual. Sets the attenuation of the external frontend. \n
			:param attenuation: float Range: depends on connected device to depends on connected device
		"""
		param = Conversions.decimal_value_to_str(attenuation)
		self._core.io.write(f'SOURce<HwInstance>:EFRontend:POWer:ATTenuation {param}')

	def get_offset(self) -> float:
		"""SCPI: [SOURce<HW>]:EFRontend:POWer:OFFSet \n
		Snippet: value: float = driver.source.efrontend.power.get_offset() \n
		Requires frontend R&S FE170ST or R&S FE110ST. Requires [SOURce<hw>]:EFRontend:AMODe AOFFset. Adds an offset value to the
		attenuation value provided from the external frontend. \n
			:return: offset: float Range: depends on connected device to depends on connected device
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:POWer:OFFSet?')
		return Conversions.str_to_float(response)

	def set_offset(self, offset: float) -> None:
		"""SCPI: [SOURce<HW>]:EFRontend:POWer:OFFSet \n
		Snippet: driver.source.efrontend.power.set_offset(offset = 1.0) \n
		Requires frontend R&S FE170ST or R&S FE110ST. Requires [SOURce<hw>]:EFRontend:AMODe AOFFset. Adds an offset value to the
		attenuation value provided from the external frontend. \n
			:param offset: float Range: depends on connected device to depends on connected device
		"""
		param = Conversions.decimal_value_to_str(offset)
		self._core.io.write(f'SOURce<HwInstance>:EFRontend:POWer:OFFSet {param}')
