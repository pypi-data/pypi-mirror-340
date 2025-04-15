from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RfCls:
	"""Rf commands group definition. 5 total commands, 2 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rf", core, parent)

	@property
	def iqModulator(self):
		"""iqModulator commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_iqModulator'):
			from .IqModulator import IqModulatorCls
			self._iqModulator = IqModulatorCls(self._core, self._cmd_group)
		return self._iqModulator

	@property
	def linearize(self):
		"""linearize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_linearize'):
			from .Linearize import LinearizeCls
			self._linearize = LinearizeCls(self._core, self._cmd_group)
		return self._linearize

	# noinspection PyTypeChecker
	def get_characteristics(self) -> enums.IqOptMode:
		"""SCPI: [SOURce<HW>]:CORRection:OPTimize:RF:CHARacteristics \n
		Snippet: value: enums.IqOptMode = driver.source.correction.optimize.rf.get_characteristics() \n
		Sets the method for optimizing the I/Q modulation. \n
			:return: characteristic: OFF| EVM | USER OFF No dedicated I/Q modulation optimization. EVM Optimizes I/Q modulation to achieve better EVM performance. This method reduces the wideband noise and improves the nonlinear effects of amplifiers resulting in a linear gain. USER Sets a user-defined optimization as the I/Q modulation method.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:OPTimize:RF:CHARacteristics?')
		return Conversions.str_to_scalar_enum(response, enums.IqOptMode)

	def set_characteristics(self, characteristic: enums.IqOptMode) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:OPTimize:RF:CHARacteristics \n
		Snippet: driver.source.correction.optimize.rf.set_characteristics(characteristic = enums.IqOptMode.EVM) \n
		Sets the method for optimizing the I/Q modulation. \n
			:param characteristic: OFF| EVM | USER OFF No dedicated I/Q modulation optimization. EVM Optimizes I/Q modulation to achieve better EVM performance. This method reduces the wideband noise and improves the nonlinear effects of amplifiers resulting in a linear gain. USER Sets a user-defined optimization as the I/Q modulation method.
		"""
		param = Conversions.enum_scalar_to_str(characteristic, enums.IqOptMode)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:OPTimize:RF:CHARacteristics {param}')

	def get_headroom(self) -> bool:
		"""SCPI: [SOURce<HW>]:CORRection:OPTimize:RF:HEADroom \n
		Snippet: value: bool = driver.source.correction.optimize.rf.get_headroom() \n
		Enables automatic adjustments of the I/Q modulator after each RF frequency change or RF level change. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:OPTimize:RF:HEADroom?')
		return Conversions.str_to_bool(response)

	def set_headroom(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:OPTimize:RF:HEADroom \n
		Snippet: driver.source.correction.optimize.rf.set_headroom(state = False) \n
		Enables automatic adjustments of the I/Q modulator after each RF frequency change or RF level change. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:OPTimize:RF:HEADroom {param}')

	def clone(self) -> 'RfCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RfCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
