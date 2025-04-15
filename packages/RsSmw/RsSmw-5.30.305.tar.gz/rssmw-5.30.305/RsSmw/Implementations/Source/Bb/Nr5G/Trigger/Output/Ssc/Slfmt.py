from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SlfmtCls:
	"""Slfmt commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("slfmt", core, parent)

	def get(self, output=repcap.Output.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TRIGger:OUTPut<CH>:SSC:SLFMt \n
		Snippet: value: int = driver.source.bb.nr5G.trigger.output.ssc.slfmt.get(output = repcap.Output.Default) \n
		Sets the special slot format index of the special slot included in a UL/DL pattern containing a marker according to . \n
			:param output: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: spec_slot_fmt_idx: integer Range: 0 to 45"""
		output_cmd_val = self._cmd_group.get_repcap_cmd_value(output, repcap.Output)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:TRIGger:OUTPut{output_cmd_val}:SSC:SLFMt?')
		return Conversions.str_to_int(response)
