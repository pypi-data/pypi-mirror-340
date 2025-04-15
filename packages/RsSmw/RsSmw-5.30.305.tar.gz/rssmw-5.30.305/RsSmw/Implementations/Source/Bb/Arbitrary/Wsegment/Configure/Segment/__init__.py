from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SegmentCls:
	"""Segment commands group definition. 5 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("segment", core, parent)

	@property
	def index(self):
		"""index commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_index'):
			from .Index import IndexCls
			self._index = IndexCls(self._core, self._cmd_group)
		return self._index

	def set_append(self, waveform: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:SEGMent:APPend \n
		Snippet: driver.source.bb.arbitrary.wsegment.configure.segment.set_append(waveform = 'abc') \n
		Appends the specified waveform to the configuration file. \n
			:param waveform: string
		"""
		param = Conversions.value_to_quoted_str(waveform)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:SEGMent:APPend {param}')

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:SEGMent:CATalog \n
		Snippet: value: List[str] = driver.source.bb.arbitrary.wsegment.configure.segment.get_catalog() \n
		Queries the segments of the currently selected configuration file. \n
			:return: catalog: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:SEGMent:CATalog?')
		return Conversions.str_to_str_list(response)

	def clone(self) -> 'SegmentCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SegmentCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
