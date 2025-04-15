from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MaximumCls:
	"""Maximum commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("maximum", core, parent)

	def get(self, externalDevice=repcap.ExternalDevice.Default) -> float:
		"""SCPI: [SOURce<HW>]:EFRontend:EXTDevice<ID>:FREQuency:MAXimum \n
		Snippet: value: float = driver.source.efrontend.extDevice.frequency.maximum.get(externalDevice = repcap.ExternalDevice.Default) \n
		Queries the maximum value of the frequency of the connected external device. \n
			:param externalDevice: optional repeated capability selector. Default value: Nr1 (settable in the interface 'ExtDevice')
			:return: freq_conv_fes_pi_freq_max: No help available"""
		externalDevice_cmd_val = self._cmd_group.get_repcap_cmd_value(externalDevice, repcap.ExternalDevice)
		response = self._core.io.query_str(f'SOURce<HwInstance>:EFRontend:EXTDevice{externalDevice_cmd_val}:FREQuency:MAXimum?')
		return Conversions.str_to_float(response)
