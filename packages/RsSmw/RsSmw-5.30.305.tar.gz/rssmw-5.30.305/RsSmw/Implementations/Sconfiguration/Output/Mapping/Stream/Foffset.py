from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FoffsetCls:
	"""Foffset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("foffset", core, parent)

	def set(self, sm_freq_offset: float, stream=repcap.Stream.Default) -> None:
		"""SCPI: SCONfiguration:OUTPut:MAPPing:STReam<ST>:FOFFset \n
		Snippet: driver.sconfiguration.output.mapping.stream.foffset.set(sm_freq_offset = 1.0, stream = repcap.Stream.Default) \n
		For wideband instruments (R&S SMW-B9) , this settings requires analog signal outputs: SCONfiguration:OUTPut:MODE ANAL
		Sets the frequency offset per stream. This offset implies a shift in the frequency domain for all signals that the stream
		routes to a specific output connector. For example, RF or I/Q output connectors. Value ranges depend on installed options.
		For more information, refer to the specifications document. \n
			:param sm_freq_offset: float Range: depends on options
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Stream')
		"""
		param = Conversions.decimal_value_to_str(sm_freq_offset)
		stream_cmd_val = self._cmd_group.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SCONfiguration:OUTPut:MAPPing:STReam{stream_cmd_val}:FOFFset {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""SCPI: SCONfiguration:OUTPut:MAPPing:STReam<ST>:FOFFset \n
		Snippet: value: float = driver.sconfiguration.output.mapping.stream.foffset.get(stream = repcap.Stream.Default) \n
		For wideband instruments (R&S SMW-B9) , this settings requires analog signal outputs: SCONfiguration:OUTPut:MODE ANAL
		Sets the frequency offset per stream. This offset implies a shift in the frequency domain for all signals that the stream
		routes to a specific output connector. For example, RF or I/Q output connectors. Value ranges depend on installed options.
		For more information, refer to the specifications document. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Stream')
			:return: sm_freq_offset: float Range: depends on options"""
		stream_cmd_val = self._cmd_group.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SCONfiguration:OUTPut:MAPPing:STReam{stream_cmd_val}:FOFFset?')
		return Conversions.str_to_float(response)
