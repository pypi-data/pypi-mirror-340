from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CatalogCls:
	"""Catalog commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("catalog", core, parent)

	@property
	def length(self):
		"""length commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_length'):
			from .Length import LengthCls
			self._length = LengthCls(self._core, self._cmd_group)
		return self._length

	def get_value(self) -> str:
		"""SCPI: MMEMory:CATalog \n
		Snippet: value: str = driver.massMemory.catalog.get_value() \n
		Returns the content of a particular directory. \n
			:return: catalog: string String parameter to specify the directory. If you leave out the path, the command returns the contents of the directory selected with method RsSmw.MassMemory.currentDirectory. The path may be relative or absolute.
		"""
		response = self._core.io.query_str('MMEMory:CATalog?')
		return trim_str_response(response)

	def clone(self) -> 'CatalogCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CatalogCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
