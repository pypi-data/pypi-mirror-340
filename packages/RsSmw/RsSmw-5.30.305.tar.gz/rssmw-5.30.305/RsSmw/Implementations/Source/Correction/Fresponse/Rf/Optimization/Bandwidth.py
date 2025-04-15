from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BandwidthCls:
	"""Bandwidth commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bandwidth", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AutoManualMode:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:OPTimization:BANDwidth:MODE \n
		Snippet: value: enums.AutoManualMode = driver.source.correction.fresponse.rf.optimization.bandwidth.get_mode() \n
		For high-quality I/Q modulation optimizations, sets the mode to set the signal bandwidth To enable these optimizations,
		see the following command: [:SOURce<hw>]:CORRection:FRESponse:RF:OPTimization:MODE \n
			:return: freq_resp_opt_bw_mo: AUTO| MANual AUTO Automatic bandwidth settings MANual Manual bandwidth setting via the following command: [:SOURcehw]:CORRection:FRESponse:RF:OPTimization:BANDwidth[:VALue]
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:FRESponse:RF:OPTimization:BANDwidth:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AutoManualMode)

	def set_mode(self, freq_resp_opt_bw_mo: enums.AutoManualMode) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:OPTimization:BANDwidth:MODE \n
		Snippet: driver.source.correction.fresponse.rf.optimization.bandwidth.set_mode(freq_resp_opt_bw_mo = enums.AutoManualMode.AUTO) \n
		For high-quality I/Q modulation optimizations, sets the mode to set the signal bandwidth To enable these optimizations,
		see the following command: [:SOURce<hw>]:CORRection:FRESponse:RF:OPTimization:MODE \n
			:param freq_resp_opt_bw_mo: AUTO| MANual AUTO Automatic bandwidth settings MANual Manual bandwidth setting via the following command: [:SOURcehw]:CORRection:FRESponse:RF:OPTimization:BANDwidth[:VALue]
		"""
		param = Conversions.enum_scalar_to_str(freq_resp_opt_bw_mo, enums.AutoManualMode)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:RF:OPTimization:BANDwidth:MODE {param}')

	def get_value(self) -> int:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:OPTimization:BANDwidth:[VALue] \n
		Snippet: value: int = driver.source.correction.fresponse.rf.optimization.bandwidth.get_value() \n
		Sets the signal compensation for manual bandwidth mode.
		See [:SOURce<hw>]:CORRection:FRESponse:RF:OPTimization:BANDwidth:MODE. For more information, refer to the specifications
		document. \n
			:return: freq_resp_opt_bw_va: integer Range: depends on options to depends on options * e.g. 8E6 to 120E6 (R&S SMW-B10) ; min value also depends on the system configuration (R&S SMW-B9)
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:FRESponse:RF:OPTimization:BANDwidth:VALue?')
		return Conversions.str_to_int(response)

	def set_value(self, freq_resp_opt_bw_va: int) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:OPTimization:BANDwidth:[VALue] \n
		Snippet: driver.source.correction.fresponse.rf.optimization.bandwidth.set_value(freq_resp_opt_bw_va = 1) \n
		Sets the signal compensation for manual bandwidth mode.
		See [:SOURce<hw>]:CORRection:FRESponse:RF:OPTimization:BANDwidth:MODE. For more information, refer to the specifications
		document. \n
			:param freq_resp_opt_bw_va: integer Range: depends on options to depends on options * e.g. 8E6 to 120E6 (R&S SMW-B10) ; min value also depends on the system configuration (R&S SMW-B9)
		"""
		param = Conversions.decimal_value_to_str(freq_resp_opt_bw_va)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:RF:OPTimization:BANDwidth:VALue {param}')
