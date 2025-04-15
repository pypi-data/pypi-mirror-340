from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PindexCls:
	"""Pindex commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pindex", core, parent)

	def set(self, pindex: int, output=repcap.Output.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:TRIGger:OUTPut<CH>:PINDex \n
		Snippet: driver.source.bb.btooth.trigger.output.pindex.set(pindex = 1, output = repcap.Output.Default) \n
		For Bluetooth LE data packets higher than one, sets the packet index. The index corresponds to the transmitted Tx event
		during the connection interval. \n
			:param pindex: integer Range: 1 to depends on 'No. Of Tx Packets/Event' parameter
			:param output: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
		"""
		param = Conversions.decimal_value_to_str(pindex)
		output_cmd_val = self._cmd_group.get_repcap_cmd_value(output, repcap.Output)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:TRIGger:OUTPut{output_cmd_val}:PINDex {param}')

	def get(self, output=repcap.Output.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:TRIGger:OUTPut<CH>:PINDex \n
		Snippet: value: int = driver.source.bb.btooth.trigger.output.pindex.get(output = repcap.Output.Default) \n
		For Bluetooth LE data packets higher than one, sets the packet index. The index corresponds to the transmitted Tx event
		during the connection interval. \n
			:param output: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: pindex: integer Range: 1 to depends on 'No. Of Tx Packets/Event' parameter"""
		output_cmd_val = self._cmd_group.get_repcap_cmd_value(output, repcap.Output)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:TRIGger:OUTPut{output_cmd_val}:PINDex?')
		return Conversions.str_to_int(response)
