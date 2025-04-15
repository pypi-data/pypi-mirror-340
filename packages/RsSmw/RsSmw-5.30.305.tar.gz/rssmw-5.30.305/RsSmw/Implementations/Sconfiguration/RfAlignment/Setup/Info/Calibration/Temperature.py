from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TemperatureCls:
	"""Temperature commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("temperature", core, parent)

	def get_offset(self) -> float:
		"""SCPI: SCONfiguration:RFALignment:SETup:INFO:CALibration:TEMPerature:OFFSet \n
		Snippet: value: float = driver.sconfiguration.rfAlignment.setup.info.calibration.temperature.get_offset() \n
		Queries the difference in temperature since the moment the calibration described in the loaded setup file is performed. \n
			:return: temp_offset: float
		"""
		response = self._core.io.query_str('SCONfiguration:RFALignment:SETup:INFO:CALibration:TEMPerature:OFFSet?')
		return Conversions.str_to_float(response)
