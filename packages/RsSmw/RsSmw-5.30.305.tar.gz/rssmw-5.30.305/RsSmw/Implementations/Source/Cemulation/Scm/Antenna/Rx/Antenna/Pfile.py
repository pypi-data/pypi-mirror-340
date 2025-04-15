from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PfileCls:
	"""Pfile commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pfile", core, parent)

	def set(self, filename: str, index=repcap.Index.Default) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:ANTenna:RX:ANTenna<DI>:PFILe \n
		Snippet: driver.source.cemulation.scm.antenna.rx.antenna.pfile.set(filename = 'abc', index = repcap.Index.Default) \n
		No command help available \n
			:param filename: No help available
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Antenna')
		"""
		param = Conversions.value_to_quoted_str(filename)
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:SCM:ANTenna:RX:ANTenna{index_cmd_val}:PFILe {param}')

	def get(self, index=repcap.Index.Default) -> str:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:ANTenna:RX:ANTenna<DI>:PFILe \n
		Snippet: value: str = driver.source.cemulation.scm.antenna.rx.antenna.pfile.get(index = repcap.Index.Default) \n
		No command help available \n
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Antenna')
			:return: filename: No help available"""
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		response = self._core.io.query_str(f'SOURce<HwInstance>:CEMulation:SCM:ANTenna:RX:ANTenna{index_cmd_val}:PFILe?')
		return trim_str_response(response)
