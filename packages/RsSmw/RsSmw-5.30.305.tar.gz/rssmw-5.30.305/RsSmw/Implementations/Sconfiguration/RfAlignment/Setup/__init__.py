from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SetupCls:
	"""Setup commands group definition. 25 total commands, 3 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("setup", core, parent)

	@property
	def file(self):
		"""file commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_file'):
			from .File import FileCls
			self._file = FileCls(self._core, self._cmd_group)
		return self._file

	@property
	def info(self):
		"""info commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_info'):
			from .Info import InfoCls
			self._info = InfoCls(self._core, self._cmd_group)
		return self._info

	@property
	def predefined(self):
		"""predefined commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_predefined'):
			from .Predefined import PredefinedCls
			self._predefined = PredefinedCls(self._core, self._cmd_group)
		return self._predefined

	def get_catalog(self) -> List[str]:
		"""SCPI: SCONfiguration:RFALignment:SETup:CATalog \n
		Snippet: value: List[str] = driver.sconfiguration.rfAlignment.setup.get_catalog() \n
		Queries the names of the existing setup files in the default directory. Per default, the instrument saves user-defined
		files in the /var/user/ directory. Use the command method RsSmw.MassMemory.currentDirectory to change the default
		directory to the currently used one. Only files with extension *.rfsa are listed. \n
			:return: rf_port_setup_file_cat_name: No help available
		"""
		response = self._core.io.query_str('SCONfiguration:RFALignment:SETup:CATalog?')
		return Conversions.str_to_str_list(response)

	# noinspection PyTypeChecker
	def get_status(self) -> enums.RfPortStatus:
		"""SCPI: SCONfiguration:RFALignment:SETup:STATus \n
		Snippet: value: enums.RfPortStatus = driver.sconfiguration.rfAlignment.setup.get_status() \n
		Queries information on the internal compensation status and the connected secondary instruments. \n
			:return: setup_status: NALign| ALIGned| ERRor| WARNing| INACtive| NOSetup| INValid NOSetup = Setup is not loaded INValid = Loaded setup does not match the current setup INACtive = Setup loaded but RF port alignment not enabled NALign = Setup is loaded but aligned not triggered ALIGned | ERRor | WARNing = Setup is aligned, error, warning
		"""
		response = self._core.io.query_str('SCONfiguration:RFALignment:SETup:STATus?')
		return Conversions.str_to_scalar_enum(response, enums.RfPortStatus)

	def clone(self) -> 'SetupCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SetupCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
