from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IqCls:
	"""Iq commands group definition. 215 total commands, 5 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iq", core, parent)

	@property
	def doherty(self):
		"""doherty commands group. 11 Sub-classes, 2 commands."""
		if not hasattr(self, '_doherty'):
			from .Doherty import DohertyCls
			self._doherty = DohertyCls(self._core, self._cmd_group)
		return self._doherty

	@property
	def dpd(self):
		"""dpd commands group. 10 Sub-classes, 5 commands."""
		if not hasattr(self, '_dpd'):
			from .Dpd import DpdCls
			self._dpd = DpdCls(self._core, self._cmd_group)
		return self._dpd

	@property
	def impairment(self):
		"""impairment commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_impairment'):
			from .Impairment import ImpairmentCls
			self._impairment = ImpairmentCls(self._core, self._cmd_group)
		return self._impairment

	@property
	def output(self):
		"""output commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_output'):
			from .Output import OutputCls
			self._output = OutputCls(self._core, self._cmd_group)
		return self._output

	@property
	def swap(self):
		"""swap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_swap'):
			from .Swap import SwapCls
			self._swap = SwapCls(self._core, self._cmd_group)
		return self._swap

	def get_crest_factor(self) -> float:
		"""SCPI: [SOURce<HW>]:IQ:CREStfactor \n
		Snippet: value: float = driver.source.iq.get_crest_factor() \n
		Specifies the crest factor for the external analog signal. \n
			:return: crest_factor: float Range: 0 to 35, Unit: dB
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:CREStfactor?')
		return Conversions.str_to_float(response)

	def set_crest_factor(self, crest_factor: float) -> None:
		"""SCPI: [SOURce<HW>]:IQ:CREStfactor \n
		Snippet: driver.source.iq.set_crest_factor(crest_factor = 1.0) \n
		Specifies the crest factor for the external analog signal. \n
			:param crest_factor: float Range: 0 to 35, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(crest_factor)
		self._core.io.write(f'SOURce<HwInstance>:IQ:CREStfactor {param}')

	# noinspection PyTypeChecker
	def get_gain(self) -> enums.IqGainAll:
		"""SCPI: [SOURce<HW>]:IQ:GAIN \n
		Snippet: value: enums.IqGainAll = driver.source.iq.get_gain() \n
		Sets the baseband gain for a wide dynamic range. You can amplify the baseband signal power level (positive gain) or
		attenuate this level (negative gain) to optimize the I/Q modulation performance. The optimization is a trade-off between
		signal distortion and signal-to-noise ratio (SNR) . \n
			:return: gain: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:GAIN?')
		return Conversions.str_to_scalar_enum(response, enums.IqGainAll)

	def set_gain(self, gain: enums.IqGainAll) -> None:
		"""SCPI: [SOURce<HW>]:IQ:GAIN \n
		Snippet: driver.source.iq.set_gain(gain = enums.IqGainAll.AUTO) \n
		Sets the baseband gain for a wide dynamic range. You can amplify the baseband signal power level (positive gain) or
		attenuate this level (negative gain) to optimize the I/Q modulation performance. The optimization is a trade-off between
		signal distortion and signal-to-noise ratio (SNR) . \n
			:param gain: DBM4| DBM2| DB0| DB2| DB4| DB8| DB6| DBM3| DB3| AUTO Dynamic range of 16 dB divided into 2 dB steps. DBM2|DBM4 '-4 dB'/'-2 dB' Attenuates the baseband signal internally to minimize signal distortions and optimize the intermodulation characteristics of the modulated signal. But the SNR decreases, the signal noise increases. DB0 0 dB No changes on the baseband signal, applies no optimization. DB2|DB4|DB6|DB8 '2 dB'/'4 dB'/'6 dB'/'8 dB' Amplifies the baseband signal internally to maximize the SNR while minimizing the signal noise is minimized. But the signal distortions increase. DBM3|DB3 (Setting only) Provided only for backward compatibility with other Rohde & Schwarz signal generators. The R&S SMW200A accepts these values and maps them automatically as follows: DBM3 = DBM2, DB3 = DB2 AUTO Requires a connected R&S SZU. The R&S SMW200A automatically sets the gain with optimized adjustment data from the R&S SZU.
		"""
		param = Conversions.enum_scalar_to_str(gain, enums.IqGainAll)
		self._core.io.write(f'SOURce<HwInstance>:IQ:GAIN {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.IqSour:
		"""SCPI: [SOURce<HW>]:IQ:SOURce \n
		Snippet: value: enums.IqSour = driver.source.iq.get_source() \n
		Selects the input signal source for the I/Q modulator. \n
			:return: source: BASeband | | ANALog| DIFFerential BASeband Internal baseband signal ANALog External analog wideband I/Q signal Enabling the I/Q modulator disables an enabled amplitude modulation of the RF output signal. Differential External analog wideband I/Q signal Enabling the I/Q modulator disables an enabled amplitude modulation of the RF output signal.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.IqSour)

	def set_source(self, source: enums.IqSour) -> None:
		"""SCPI: [SOURce<HW>]:IQ:SOURce \n
		Snippet: driver.source.iq.set_source(source = enums.IqSour.ANALog) \n
		Selects the input signal source for the I/Q modulator. \n
			:param source: BASeband | | ANALog| DIFFerential BASeband Internal baseband signal ANALog External analog wideband I/Q signal Enabling the I/Q modulator disables an enabled amplitude modulation of the RF output signal. Differential External analog wideband I/Q signal Enabling the I/Q modulator disables an enabled amplitude modulation of the RF output signal.
		"""
		param = Conversions.enum_scalar_to_str(source, enums.IqSour)
		self._core.io.write(f'SOURce<HwInstance>:IQ:SOURce {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:IQ:STATe \n
		Snippet: value: bool = driver.source.iq.get_state() \n
		Enables the I/Q modulation. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:IQ:STATe \n
		Snippet: driver.source.iq.set_state(state = False) \n
		Enables the I/Q modulation. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:IQ:STATe {param}')

	def get_wb_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:IQ:WBSTate \n
		Snippet: value: bool = driver.source.iq.get_wb_state() \n
		Activates I/Q wideband mode. Activation automatically optimizes the settings for wideband modulation signals with a
		bandwidth that is higher then 5 MHz. \n
			:return: wb_state: 1| ON| 0| OFF *RST: 0 (R&S SMW-B10) / 1 (R&S SMW-B9)
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:WBSTate?')
		return Conversions.str_to_bool(response)

	def set_wb_state(self, wb_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:IQ:WBSTate \n
		Snippet: driver.source.iq.set_wb_state(wb_state = False) \n
		Activates I/Q wideband mode. Activation automatically optimizes the settings for wideband modulation signals with a
		bandwidth that is higher then 5 MHz. \n
			:param wb_state: 1| ON| 0| OFF *RST: 0 (R&S SMW-B10) / 1 (R&S SMW-B9)
		"""
		param = Conversions.bool_to_str(wb_state)
		self._core.io.write(f'SOURce<HwInstance>:IQ:WBSTate {param}')

	def clone(self) -> 'IqCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IqCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
