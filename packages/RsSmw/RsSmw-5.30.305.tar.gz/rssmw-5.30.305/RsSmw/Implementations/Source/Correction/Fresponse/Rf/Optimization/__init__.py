from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OptimizationCls:
	"""Optimization commands group definition. 5 total commands, 3 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("optimization", core, parent)

	@property
	def bandwidth(self):
		"""bandwidth commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_bandwidth'):
			from .Bandwidth import BandwidthCls
			self._bandwidth = BandwidthCls(self._core, self._cmd_group)
		return self._bandwidth

	@property
	def hold(self):
		"""hold commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hold'):
			from .Hold import HoldCls
			self._hold = HoldCls(self._core, self._cmd_group)
		return self._hold

	@property
	def local(self):
		"""local commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_local'):
			from .Local import LocalCls
			self._local = LocalCls(self._core, self._cmd_group)
		return self._local

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.BbImpOptModeRangeFresponse:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:OPTimization:MODE \n
		Snippet: value: enums.BbImpOptModeRangeFresponse = driver.source.correction.fresponse.rf.optimization.get_mode() \n
		Sets the optimization mode for frequency response correction. This optimization mode also uses the I/Q modulator and vice
		versa via the command: SOURce<hw>:BB:IMPairment:OPTimization:MODE See 'Optimization Mode'. \n
			:return: freq_resp_opt_mode: FAST| QHIGh | QHTable FAST Optimization by compensation for I/Q skew. QHTable Requires an active connection between an R&S SZU and the R&S SMW200A. Improves optimization while maintaining the modulation speed. QHIGh Optimization by compensation for I/Q skew and frequency response correction. This mode interrupts the RF signal. Do not use it in combination with the uninterrupted level settings and strictly monotone modes RF level modes. These RF level modes can be set with the following command: [:SOURcehw]:POWer:LBEHaviour *RST: QHIGh or QHTable with an R&S SZU connected, see above.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:FRESponse:RF:OPTimization:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.BbImpOptModeRangeFresponse)

	def set_mode(self, freq_resp_opt_mode: enums.BbImpOptModeRangeFresponse) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:OPTimization:MODE \n
		Snippet: driver.source.correction.fresponse.rf.optimization.set_mode(freq_resp_opt_mode = enums.BbImpOptModeRangeFresponse.FAST) \n
		Sets the optimization mode for frequency response correction. This optimization mode also uses the I/Q modulator and vice
		versa via the command: SOURce<hw>:BB:IMPairment:OPTimization:MODE See 'Optimization Mode'. \n
			:param freq_resp_opt_mode: FAST| QHIGh | QHTable FAST Optimization by compensation for I/Q skew. QHTable Requires an active connection between an R&S SZU and the R&S SMW200A. Improves optimization while maintaining the modulation speed. QHIGh Optimization by compensation for I/Q skew and frequency response correction. This mode interrupts the RF signal. Do not use it in combination with the uninterrupted level settings and strictly monotone modes RF level modes. These RF level modes can be set with the following command: [:SOURcehw]:POWer:LBEHaviour *RST: QHIGh or QHTable with an R&S SZU connected, see above.
		"""
		param = Conversions.enum_scalar_to_str(freq_resp_opt_mode, enums.BbImpOptModeRangeFresponse)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:RF:OPTimization:MODE {param}')

	def clone(self) -> 'OptimizationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = OptimizationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
