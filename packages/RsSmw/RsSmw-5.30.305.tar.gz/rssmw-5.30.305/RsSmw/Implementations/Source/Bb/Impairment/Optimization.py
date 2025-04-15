from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OptimizationCls:
	"""Optimization commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("optimization", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.BbImpOptMode:
		"""SCPI: [SOURce<HW>]:BB:IMPairment:OPTimization:MODE \n
		Snippet: value: enums.BbImpOptMode = driver.source.bb.impairment.optimization.get_mode() \n
		Sets the optimization mode for I/Q modulation. If equipped with option R&S SMW-K544, the optimization mode applies for
		the I/Q modulation performance and for the user-defined frequency response corrections. See 'User-defined correction
		settings'. \n
			:return: mode: FAST| | QHIGh | QHTable FAST Fast optimization with high switching speed by compensating for I/Q skew. This mode is suitable in time sensitive environments and for narrowband signals. QHIGh Optimization by compensating for I/Q skew and frequency response correction. This mode interrupts the RF signal generation. Do not use it in combination with the uninterrupted level settings and strictly monotone modes RF level modes. See [:SOURcehw]:POWer:LBEHaviour. QHTable Improves the frequency response while maintaining setting time, there is no signal interruption. *RST: FAST for R&S SMW-B10) / QHIGh for R&S SMW-B9 / QHTable if the R&S SMW200A generates upconverted I/Q signal with a connected R&S SZU connected.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:IMPairment:OPTimization:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.BbImpOptMode)

	def set_mode(self, mode: enums.BbImpOptMode) -> None:
		"""SCPI: [SOURce<HW>]:BB:IMPairment:OPTimization:MODE \n
		Snippet: driver.source.bb.impairment.optimization.set_mode(mode = enums.BbImpOptMode.FAST) \n
		Sets the optimization mode for I/Q modulation. If equipped with option R&S SMW-K544, the optimization mode applies for
		the I/Q modulation performance and for the user-defined frequency response corrections. See 'User-defined correction
		settings'. \n
			:param mode: FAST| | QHIGh | QHTable FAST Fast optimization with high switching speed by compensating for I/Q skew. This mode is suitable in time sensitive environments and for narrowband signals. QHIGh Optimization by compensating for I/Q skew and frequency response correction. This mode interrupts the RF signal generation. Do not use it in combination with the uninterrupted level settings and strictly monotone modes RF level modes. See [:SOURcehw]:POWer:LBEHaviour. QHTable Improves the frequency response while maintaining setting time, there is no signal interruption. *RST: FAST for R&S SMW-B10) / QHIGh for R&S SMW-B9 / QHTable if the R&S SMW200A generates upconverted I/Q signal with a connected R&S SZU connected.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.BbImpOptMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:IMPairment:OPTimization:MODE {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:IMPairment:OPTimization:STATe \n
		Snippet: value: bool = driver.source.bb.impairment.optimization.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:IMPairment:OPTimization:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:IMPairment:OPTimization:STATe \n
		Snippet: driver.source.bb.impairment.optimization.set_state(state = False) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:IMPairment:OPTimization:STATe {param}')
