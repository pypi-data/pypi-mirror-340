from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InitializationCls:
	"""Initialization commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("initialization", core, parent)

	@property
	def predefined(self):
		"""predefined commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_predefined'):
			from .Predefined import PredefinedCls
			self._predefined = PredefinedCls(self._core, self._cmd_group)
		return self._predefined

	def get_catalog(self) -> List[str]:
		"""SCPI: SCONfiguration:EXTernal:REMote:INITialization:CATalog \n
		Snippet: value: List[str] = driver.sconfiguration.external.remote.initialization.get_catalog() \n
		Queries the names of the existing initialization files in the default directory. Per default, the instrument saves
		user-defined files in the /var/user/ directory. Use the command method RsSmw.MassMemory.currentDirectory to change the
		default directory to the currently used one. Only files with extension *.iec are listed. \n
			:return: rf_rem_ctrl_scpi_init_cat_name_user: No help available
		"""
		response = self._core.io.query_str('SCONfiguration:EXTernal:REMote:INITialization:CATalog?')
		return Conversions.str_to_str_list(response)

	def clone(self) -> 'InitializationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = InitializationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
