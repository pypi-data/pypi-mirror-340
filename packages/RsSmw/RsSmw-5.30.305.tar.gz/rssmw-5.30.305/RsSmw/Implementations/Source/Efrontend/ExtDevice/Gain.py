from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GainCls:
	"""Gain commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("gain", core, parent)

	def get(self, externalDevice=repcap.ExternalDevice.Default) -> float:
		"""SCPI: [SOURce<HW>]:EFRontend:EXTDevice<ID>:GAIN \n
		Snippet: value: float = driver.source.efrontend.extDevice.gain.get(externalDevice = repcap.ExternalDevice.Default) \n
		Queries the gain of the amplifier connected as external device. \n
			:param externalDevice: optional repeated capability selector. Default value: Nr1 (settable in the interface 'ExtDevice')
			:return: gain: float"""
		externalDevice_cmd_val = self._cmd_group.get_repcap_cmd_value(externalDevice, repcap.ExternalDevice)
		response = self._core.io.query_str(f'SOURce<HwInstance>:EFRontend:EXTDevice{externalDevice_cmd_val}:GAIN?')
		return Conversions.str_to_float(response)
