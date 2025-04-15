from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LhdrCls:
	"""Lhdr commands group definition. 3 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lhdr", core, parent)

	@property
	def addp(self):
		"""addp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_addp'):
			from .Addp import AddpCls
			self._addp = AddpCls(self._core, self._cmd_group)
		return self._addp

	@property
	def pagr(self):
		"""pagr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pagr'):
			from .Pagr import PagrCls
			self._pagr = PagrCls(self._core, self._cmd_group)
		return self._pagr

	# noinspection PyTypeChecker
	def get_gi_type(self) -> enums.SequenceLength:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:LHDR:GITYpe \n
		Snippet: value: enums.SequenceLength = driver.source.bb.wlay.pconfig.lhdr.get_gi_type() \n
		Selects the type of the guard interval (GI) . You can select between GI types short, normal or long. \n
			:return: gi_type: SHORT| NORMAL| LONG
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:LHDR:GITYpe?')
		return Conversions.str_to_scalar_enum(response, enums.SequenceLength)

	def set_gi_type(self, gi_type: enums.SequenceLength) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:LHDR:GITYpe \n
		Snippet: driver.source.bb.wlay.pconfig.lhdr.set_gi_type(gi_type = enums.SequenceLength.LONG) \n
		Selects the type of the guard interval (GI) . You can select between GI types short, normal or long. \n
			:param gi_type: SHORT| NORMAL| LONG
		"""
		param = Conversions.enum_scalar_to_str(gi_type, enums.SequenceLength)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:LHDR:GITYpe {param}')

	def clone(self) -> 'LhdrCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LhdrCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
