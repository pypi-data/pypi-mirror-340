from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IqModulatorCls:
	"""IqModulator commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iqModulator", core, parent)

	def get_adjust(self) -> bool:
		"""SCPI: [SOURce<HW>]:CORRection:OPTimize:RF:IQModulator:ADJust \n
		Snippet: value: bool = driver.source.correction.optimize.rf.iqModulator.get_adjust() \n
		Enables automatic adjustments of the I/Q modulator after each RF frequency change or RF level change. \n
			:return: adjust_error: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:OPTimize:RF:IQModulator:ADJust?')
		return Conversions.str_to_bool(response)

	def get_value(self) -> bool:
		"""SCPI: [SOURce<HW>]:CORRection:OPTimize:RF:IQModulator \n
		Snippet: value: bool = driver.source.correction.optimize.rf.iqModulator.get_value() \n
		Enables adjustments of the I/Q modulator after each RF frequency change or RF level change. \n
			:return: state: 1| ON| 0| OFF 1|ON Adjusts the I/Q modulator during modulation after each RF frequency change or RF level change. 0|OFF No adjustments of the I/Q modulator during modulation.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:OPTimize:RF:IQModulator?')
		return Conversions.str_to_bool(response)

	def set_value(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:OPTimize:RF:IQModulator \n
		Snippet: driver.source.correction.optimize.rf.iqModulator.set_value(state = False) \n
		Enables adjustments of the I/Q modulator after each RF frequency change or RF level change. \n
			:param state: 1| ON| 0| OFF 1|ON Adjusts the I/Q modulator during modulation after each RF frequency change or RF level change. 0|OFF No adjustments of the I/Q modulator during modulation.
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:OPTimize:RF:IQModulator {param}')
