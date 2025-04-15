from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AlignCls:
	"""Align commands group definition. 3 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("align", core, parent)

	@property
	def rfports(self):
		"""rfports commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_rfports'):
			from .Rfports import RfportsCls
			self._rfports = RfportsCls(self._core, self._cmd_group)
		return self._rfports

	# noinspection PyTypeChecker
	def get_status(self) -> enums.BwExtAlignStatus:
		"""SCPI: SCONfiguration:BEXTension:ALIGn:STATus \n
		Snippet: value: enums.BwExtAlignStatus = driver.sconfiguration.bextension.align.get_status() \n
		Queries the alignment status of the bandwidth extension setup. \n
			:return: aligned_status: NALigned| ALIGned NALigned Setup is not aligned. ALIGned Setup is aligned.
		"""
		response = self._core.io.query_str('SCONfiguration:BEXTension:ALIGn:STATus?')
		return Conversions.str_to_scalar_enum(response, enums.BwExtAlignStatus)

	def clone(self) -> 'AlignCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AlignCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
