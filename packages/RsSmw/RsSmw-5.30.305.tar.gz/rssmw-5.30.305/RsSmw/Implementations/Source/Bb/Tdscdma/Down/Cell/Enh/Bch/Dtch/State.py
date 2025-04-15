from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def get(self, cell=repcap.Cell.Default, channel=repcap.Channel.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:BCH:DTCH<CH>:STATe \n
		Snippet: value: bool = driver.source.bb.tdscdma.down.cell.enh.bch.dtch.state.get(cell = repcap.Cell.Default, channel = repcap.Channel.Default) \n
		Queries the state of the transport channel. \n
			:param cell: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dtch')
			:return: state: 1| ON| 0| OFF"""
		cell_cmd_val = self._cmd_group.get_repcap_cmd_value(cell, repcap.Cell)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{cell_cmd_val}:ENH:BCH:DTCH{channel_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
