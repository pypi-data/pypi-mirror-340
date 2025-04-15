from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MmiStepsCls:
	"""MmiSteps commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mmiSteps", core, parent)

	def set(self, mm_min_steps: int, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:MMISteps \n
		Snippet: driver.source.bb.btooth.cs.sevent.mmiSteps.set(mm_min_steps = 1, channelNull = repcap.ChannelNull.Default) \n
		Sets the minimum number of main mode steps. \n
			:param mm_min_steps: integer Range: 2 to 255
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
		"""
		param = Conversions.decimal_value_to_str(mm_min_steps)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:MMISteps {param}')

	def get(self, channelNull=repcap.ChannelNull.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:MMISteps \n
		Snippet: value: int = driver.source.bb.btooth.cs.sevent.mmiSteps.get(channelNull = repcap.ChannelNull.Default) \n
		Sets the minimum number of main mode steps. \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:return: mm_min_steps: integer Range: 2 to 255"""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:MMISteps?')
		return Conversions.str_to_int(response)
