from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MtypeCls:
	"""Mtype commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mtype", core, parent)

	# noinspection PyTypeChecker
	def get(self, channelNull=repcap.ChannelNull.Default, stepNull=repcap.StepNull.Default) -> enums.BtoCsModeType:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:[STEP<ST0>]:MTYPe \n
		Snippet: value: enums.BtoCsModeType = driver.source.bb.btooth.cs.sevent.step.mtype.get(channelNull = repcap.ChannelNull.Default, stepNull = repcap.StepNull.Default) \n
		Queries the mode type for individual CS steps. For the first CS step, the mode type is the Mode-0. For the other CS steps,
		the mode type is the main mode in the CS step configuration. \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:param stepNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Step')
			:return: mode_type: MODE0| MODE1| MODE2| MODE3 For a description, see [:SOURcehw]:BB:BTOoth:CS[:SEVentch0]:MMODe."""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		stepNull_cmd_val = self._cmd_group.get_repcap_cmd_value(stepNull, repcap.StepNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:STEP{stepNull_cmd_val}:MTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsModeType)
