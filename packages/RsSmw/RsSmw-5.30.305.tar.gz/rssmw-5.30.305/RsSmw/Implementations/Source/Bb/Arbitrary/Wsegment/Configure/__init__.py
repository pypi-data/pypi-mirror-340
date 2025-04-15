from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ConfigureCls:
	"""Configure commands group definition. 17 total commands, 5 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("configure", core, parent)

	@property
	def blank(self):
		"""blank commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_blank'):
			from .Blank import BlankCls
			self._blank = BlankCls(self._core, self._cmd_group)
		return self._blank

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_clock'):
			from .Clock import ClockCls
			self._clock = ClockCls(self._core, self._cmd_group)
		return self._clock

	@property
	def level(self):
		"""level commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_level'):
			from .Level import LevelCls
			self._level = LevelCls(self._core, self._cmd_group)
		return self._level

	@property
	def marker(self):
		"""marker commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_marker'):
			from .Marker import MarkerCls
			self._marker = MarkerCls(self._core, self._cmd_group)
		return self._marker

	@property
	def segment(self):
		"""segment commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_segment'):
			from .Segment import SegmentCls
			self._segment = SegmentCls(self._core, self._cmd_group)
		return self._segment

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:CATalog \n
		Snippet: value: List[str] = driver.source.bb.arbitrary.wsegment.configure.get_catalog() \n
		Queries the available configuration files in the default directory. See also 'File concept'. \n
			:return: catalog: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_comment(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:COMMent \n
		Snippet: value: str = driver.source.bb.arbitrary.wsegment.configure.get_comment() \n
		Enters a comment for the selected configuration file. \n
			:return: comment: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:COMMent?')
		return trim_str_response(response)

	def set_comment(self, comment: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:COMMent \n
		Snippet: driver.source.bb.arbitrary.wsegment.configure.set_comment(comment = 'abc') \n
		Enters a comment for the selected configuration file. \n
			:param comment: string
		"""
		param = Conversions.value_to_quoted_str(comment)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:COMMent {param}')

	def delete(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:DELete \n
		Snippet: driver.source.bb.arbitrary.wsegment.configure.delete(filename = 'abc') \n
		Deletes the selected configuration file. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:DELete {param}')

	def get_ofile(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:OFILe \n
		Snippet: value: str = driver.source.bb.arbitrary.wsegment.configure.get_ofile() \n
		Defines the file name of the output multi-segment waveform. \n
			:return: ofile: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:OFILe?')
		return trim_str_response(response)

	def set_ofile(self, ofile: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:OFILe \n
		Snippet: driver.source.bb.arbitrary.wsegment.configure.set_ofile(ofile = 'abc') \n
		Defines the file name of the output multi-segment waveform. \n
			:param ofile: string
		"""
		param = Conversions.value_to_quoted_str(ofile)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:OFILe {param}')

	def get_select(self) -> str:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:SELect \n
		Snippet: value: str = driver.source.bb.arbitrary.wsegment.configure.get_select() \n
		Selects a configuration file from the default directory. If a configuration file with the specified name does not yet
		exist, it is created. The file extension *.inf_mswv may be omitted. \n
			:return: filename: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:SELect?')
		return trim_str_response(response)

	def set_select(self, filename: str) -> None:
		"""SCPI: [SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:SELect \n
		Snippet: driver.source.bb.arbitrary.wsegment.configure.set_select(filename = 'abc') \n
		Selects a configuration file from the default directory. If a configuration file with the specified name does not yet
		exist, it is created. The file extension *.inf_mswv may be omitted. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:SELect {param}')

	def clone(self) -> 'ConfigureCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ConfigureCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
