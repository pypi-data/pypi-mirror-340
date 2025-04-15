from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AlignCls:
	"""Align commands group definition. 7 total commands, 2 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("align", core, parent)

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def pep(self):
		"""pep commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_pep'):
			from .Pep import PepCls
			self._pep = PepCls(self._core, self._cmd_group)
		return self._pep

	def get_comment(self) -> str:
		"""SCPI: SCONfiguration:BEXTension:INFO:ALIGn:COMMent \n
		Snippet: value: str = driver.sconfiguration.bextension.info.align.get_comment() \n
		Queries commenting information on the setup alignment. The information specifies characteristics of the aligment or the
		bandwidth extension setup. \n
			:return: comment: string
		"""
		response = self._core.io.query_str('SCONfiguration:BEXTension:INFO:ALIGn:COMMent?')
		return trim_str_response(response)

	def get_date(self) -> str:
		"""SCPI: SCONfiguration:BEXTension:INFO:ALIGn:DATE \n
		Snippet: value: str = driver.sconfiguration.bextension.info.align.get_date() \n
		Queries the date of the last setup alignment procedure. \n
			:return: align_date: string
		"""
		response = self._core.io.query_str('SCONfiguration:BEXTension:INFO:ALIGn:DATE?')
		return trim_str_response(response)

	def get_time(self) -> str:
		"""SCPI: SCONfiguration:BEXTension:INFO:ALIGn:TIME \n
		Snippet: value: str = driver.sconfiguration.bextension.info.align.get_time() \n
		Queries the time of the last setup alignment procedure. \n
			:return: align_time: string
		"""
		response = self._core.io.query_str('SCONfiguration:BEXTension:INFO:ALIGn:TIME?')
		return trim_str_response(response)

	def clone(self) -> 'AlignCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AlignCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
