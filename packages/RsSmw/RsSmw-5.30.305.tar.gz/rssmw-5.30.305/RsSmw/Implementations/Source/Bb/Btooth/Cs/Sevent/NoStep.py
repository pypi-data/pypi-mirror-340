from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NoStepCls:
	"""NoStep commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("noStep", core, parent)

	def set(self, num_of_steps: int, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:NOSTep \n
		Snippet: driver.source.bb.btooth.cs.sevent.noStep.set(num_of_steps = 1, channelNull = repcap.ChannelNull.Default) \n
		Sets or display the number of CS steps. Setting requires manual step scheduling. Settable minimum values are 1 or equal
		to the number of non-zero Mode-0 steps. See also [:SOURce<hw>]:BB:BTOoth:CS:SSCHeduling. \n
			:param num_of_steps: integer Range: 2 to 160
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
		"""
		param = Conversions.decimal_value_to_str(num_of_steps)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:NOSTep {param}')

	def get(self, channelNull=repcap.ChannelNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:NOSTep \n
		Snippet: value: int = driver.source.bb.btooth.cs.sevent.noStep.get(channelNull = repcap.ChannelNull.Default) \n
		Sets or display the number of CS steps. Setting requires manual step scheduling. Settable minimum values are 1 or equal
		to the number of non-zero Mode-0 steps. See also [:SOURce<hw>]:BB:BTOoth:CS:SSCHeduling. \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:return: num_of_steps: integer Range: 2 to 160"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:NOSTep?')
		return Conversions.str_to_int(response)
