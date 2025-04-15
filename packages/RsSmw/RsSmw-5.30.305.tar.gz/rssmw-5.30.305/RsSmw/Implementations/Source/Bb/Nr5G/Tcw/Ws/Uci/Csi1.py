from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Csi1Cls:
	"""Csi1 commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("csi1", core, parent)

	def get_pattern(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:UCI:CSI1:PATTern \n
		Snippet: value: str = driver.source.bb.nr5G.tcw.ws.uci.csi1.get_pattern() \n
		Defines the frequency and time domain of the CSI part 1 subcarrier location. \n
			:return: csi_1_pattern: Nr5gPUCCHUcidataPattLenMax bits
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:WS:UCI:CSI1:PATTern?')
		return trim_str_response(response)

	def set_pattern(self, csi_1_pattern: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:WS:UCI:CSI1:PATTern \n
		Snippet: driver.source.bb.nr5G.tcw.ws.uci.csi1.set_pattern(csi_1_pattern = rawAbc) \n
		Defines the frequency and time domain of the CSI part 1 subcarrier location. \n
			:param csi_1_pattern: Nr5gPUCCHUcidataPattLenMax bits
		"""
		param = Conversions.value_to_str(csi_1_pattern)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:WS:UCI:CSI1:PATTern {param}')
