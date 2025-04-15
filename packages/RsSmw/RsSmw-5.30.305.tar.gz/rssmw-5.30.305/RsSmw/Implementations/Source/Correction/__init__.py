from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CorrectionCls:
	"""Correction commands group definition. 81 total commands, 6 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("correction", core, parent)

	@property
	def cset(self):
		"""cset commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_cset'):
			from .Cset import CsetCls
			self._cset = CsetCls(self._core, self._cmd_group)
		return self._cset

	@property
	def dexchange(self):
		"""dexchange commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_dexchange'):
			from .Dexchange import DexchangeCls
			self._dexchange = DexchangeCls(self._core, self._cmd_group)
		return self._dexchange

	@property
	def fresponse(self):
		"""fresponse commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fresponse'):
			from .Fresponse import FresponseCls
			self._fresponse = FresponseCls(self._core, self._cmd_group)
		return self._fresponse

	@property
	def mlevel(self):
		"""mlevel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mlevel'):
			from .Mlevel import MlevelCls
			self._mlevel = MlevelCls(self._core, self._cmd_group)
		return self._mlevel

	@property
	def optimize(self):
		"""optimize commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_optimize'):
			from .Optimize import OptimizeCls
			self._optimize = OptimizeCls(self._core, self._cmd_group)
		return self._optimize

	@property
	def zeroing(self):
		"""zeroing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zeroing'):
			from .Zeroing import ZeroingCls
			self._zeroing = ZeroingCls(self._core, self._cmd_group)
		return self._zeroing

	def get_value(self) -> float:
		"""SCPI: [SOURce<HW>]:CORRection:VALue \n
		Snippet: value: float = driver.source.correction.get_value() \n
		Queries the current value for user correction. \n
			:return: value: float Range: -100 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:VALue?')
		return Conversions.str_to_float(response)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:CORRection:[STATe] \n
		Snippet: value: bool = driver.source.correction.get_state() \n
		Activates user correction with the currently selected table. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:[STATe] \n
		Snippet: driver.source.correction.set_state(state = False) \n
		Activates user correction with the currently selected table. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:STATe {param}')

	def clone(self) -> 'CorrectionCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CorrectionCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
