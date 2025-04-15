from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OntimeCls:
	"""Ontime commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ontime", core, parent)

	def set(self, ontime: float, output=repcap.Output.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TRIGger:OUTPut<CH>:ONTime \n
		Snippet: driver.source.bb.gnss.trigger.output.ontime.set(ontime = 1.0, output = repcap.Output.Default) \n
		Sets the number of chips during which the marker output is on or off. \n
			:param ontime: float Range: 0.000000011 to 0.1822215935
			:param output: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
		"""
		param = Conversions.decimal_value_to_str(ontime)
		output_cmd_val = self._cmd_group.get_repcap_cmd_value(output, repcap.Output)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TRIGger:OUTPut{output_cmd_val}:ONTime {param}')

	def get(self, output=repcap.Output.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TRIGger:OUTPut<CH>:ONTime \n
		Snippet: value: float = driver.source.bb.gnss.trigger.output.ontime.get(output = repcap.Output.Default) \n
		Sets the number of chips during which the marker output is on or off. \n
			:param output: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: ontime: No help available"""
		output_cmd_val = self._cmd_group.get_repcap_cmd_value(output, repcap.Output)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:TRIGger:OUTPut{output_cmd_val}:ONTime?')
		return Conversions.str_to_float(response)
