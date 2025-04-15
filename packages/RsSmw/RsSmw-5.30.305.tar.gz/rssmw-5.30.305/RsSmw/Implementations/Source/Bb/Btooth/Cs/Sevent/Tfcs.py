from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TfcsCls:
	"""Tfcs commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tfcs", core, parent)

	def set(self, tfcs: enums.BtoCsTfcs, channelNull=repcap.ChannelNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:TFCS \n
		Snippet: driver.source.bb.btooth.cs.sevent.tfcs.set(tfcs = enums.BtoCsTfcs.TFCS_100, channelNull = repcap.ChannelNull.Default) \n
		Sets the frequency change period (T_FCS) between consecutive CS steps. The period ranges from 15 us to 150 us. \n
			:param tfcs: TFCS_15| TFCS_20| TFCS_30| TFCS_40| TFCS_50| TFCS_60| TFCS_80| TFCS_100| TFCS_120| TFCS_150 TFCS_x, x represents values in microseconds.
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
		"""
		param = Conversions.enum_scalar_to_str(tfcs, enums.BtoCsTfcs)
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:TFCS {param}')

	# noinspection PyTypeChecker
	def get(self, channelNull=repcap.ChannelNull.Default) -> enums.BtoCsTfcs:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:CS:[SEVent<CH0>]:TFCS \n
		Snippet: value: enums.BtoCsTfcs = driver.source.bb.btooth.cs.sevent.tfcs.get(channelNull = repcap.ChannelNull.Default) \n
		Sets the frequency change period (T_FCS) between consecutive CS steps. The period ranges from 15 us to 150 us. \n
			:param channelNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sevent')
			:return: tfcs: TFCS_15| TFCS_20| TFCS_30| TFCS_40| TFCS_50| TFCS_60| TFCS_80| TFCS_100| TFCS_120| TFCS_150 TFCS_x, x represents values in microseconds."""
		channelNull_cmd_val = self._cmd_group.get_repcap_cmd_value(channelNull, repcap.ChannelNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:CS:SEVent{channelNull_cmd_val}:TFCS?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCsTfcs)
