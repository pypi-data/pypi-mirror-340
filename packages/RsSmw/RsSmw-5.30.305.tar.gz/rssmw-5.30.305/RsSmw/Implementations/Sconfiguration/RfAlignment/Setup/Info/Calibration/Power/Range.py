from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RangeCls:
	"""Range commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("range", core, parent)

	def get_lower(self) -> float:
		"""SCPI: SCONfiguration:RFALignment:SETup:INFO:CALibration:POWer:RANGe:LOWer \n
		Snippet: value: float = driver.sconfiguration.rfAlignment.setup.info.calibration.power.range.get_lower() \n
		Queries the min and max frequency and PEP values that define the calibrated range. \n
			:return: pep_min: float
		"""
		response = self._core.io.query_str('SCONfiguration:RFALignment:SETup:INFO:CALibration:POWer:RANGe:LOWer?')
		return Conversions.str_to_float(response)

	def get_upper(self) -> float:
		"""SCPI: SCONfiguration:RFALignment:SETup:INFO:CALibration:POWer:RANGe:UPPer \n
		Snippet: value: float = driver.sconfiguration.rfAlignment.setup.info.calibration.power.range.get_upper() \n
		Queries the min and max frequency and PEP values that define the calibrated range. \n
			:return: pep_max: float
		"""
		response = self._core.io.query_str('SCONfiguration:RFALignment:SETup:INFO:CALibration:POWer:RANGe:UPPer?')
		return Conversions.str_to_float(response)
