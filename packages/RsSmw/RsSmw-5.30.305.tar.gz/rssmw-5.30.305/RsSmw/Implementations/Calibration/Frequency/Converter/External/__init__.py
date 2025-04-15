from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExternalCls:
	"""External commands group definition. 4 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("external", core, parent)

	@property
	def selected(self):
		"""selected commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_selected'):
			from .Selected import SelectedCls
			self._selected = SelectedCls(self._core, self._cmd_group)
		return self._selected

	def get_value(self) -> bool:
		"""SCPI: CALibration<HW>:FREQuency:CONVerter:EXTernal \n
		Snippet: value: bool = driver.calibration.frequency.converter.external.get_value() \n
		Queries the calibration state of the connected external instrument. External instrument can be for example an external
		frontend. \n
			:return: success: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('CALibration<HwInstance>:FREQuency:CONVerter:EXTernal?')
		return Conversions.str_to_bool(response)

	def clone(self) -> 'ExternalCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ExternalCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
