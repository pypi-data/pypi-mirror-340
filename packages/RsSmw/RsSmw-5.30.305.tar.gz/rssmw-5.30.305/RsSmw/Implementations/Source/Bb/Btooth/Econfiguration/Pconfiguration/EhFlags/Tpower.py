from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TpowerCls:
	"""Tpower commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tpower", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:EHFLags:TPOWer:STATe \n
		Snippet: value: bool = driver.source.bb.btooth.econfiguration.pconfiguration.ehFlags.tpower.get_state() \n
		Enables the signaling of required transmit power. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:EHFLags:TPOWer:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:EHFLags:TPOWer:STATe \n
		Snippet: driver.source.bb.btooth.econfiguration.pconfiguration.ehFlags.tpower.set_state(state = False) \n
		Enables the signaling of required transmit power. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:EHFLags:TPOWer:STATe {param}')
