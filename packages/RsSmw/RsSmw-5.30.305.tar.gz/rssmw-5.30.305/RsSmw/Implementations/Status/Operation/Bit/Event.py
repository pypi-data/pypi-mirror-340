from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Utilities import trim_str_response
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EventCls:
	"""Event commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("event", core, parent)

	def get(self, bitNumberNull=repcap.BitNumberNull.Default) -> str:
		"""SCPI: STATus:OPERation:BIT<BITNR>:[EVENt] \n
		Snippet: value: str = driver.status.operation.bit.event.get(bitNumberNull = repcap.BitNumberNull.Default) \n
		No command help available \n
			:param bitNumberNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bit')
			:return: event: No help available"""
		bitNumberNull_cmd_val = self._cmd_group.get_repcap_cmd_value(bitNumberNull, repcap.BitNumberNull)
		response = self._core.io.query_str(f'STATus:OPERation:BIT{bitNumberNull_cmd_val}:EVENt?')
		return trim_str_response(response)
