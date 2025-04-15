from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OptimizeCls:
	"""Optimize commands group definition. 6 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("optimize", core, parent)

	@property
	def rf(self):
		"""rf commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_rf'):
			from .Rf import RfCls
			self._rf = RfCls(self._core, self._cmd_group)
		return self._rf

	def get_evm(self) -> bool:
		"""SCPI: [SOURce<HW>]:CORRection:OPTimize:EVM \n
		Snippet: value: bool = driver.source.correction.optimize.get_evm() \n
		No command help available \n
			:return: optimize_evm: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:OPTimize:EVM?')
		return Conversions.str_to_bool(response)

	def set_evm(self, optimize_evm: bool) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:OPTimize:EVM \n
		Snippet: driver.source.correction.optimize.set_evm(optimize_evm = False) \n
		No command help available \n
			:param optimize_evm: No help available
		"""
		param = Conversions.bool_to_str(optimize_evm)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:OPTimize:EVM {param}')

	def clone(self) -> 'OptimizeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = OptimizeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
