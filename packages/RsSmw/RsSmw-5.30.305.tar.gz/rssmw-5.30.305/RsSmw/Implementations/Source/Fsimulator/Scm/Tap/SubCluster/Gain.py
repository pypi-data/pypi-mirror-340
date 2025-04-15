from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GainCls:
	"""Gain commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("gain", core, parent)

	def set(self, gain: float, mimoTap=repcap.MimoTap.Default, subCluster=repcap.SubCluster.Default) -> None:
		"""SCPI: [SOURce<HW>]:FSIMulator:SCM:TAP<ST>:SUBCluster<DI>:GAIN \n
		Snippet: driver.source.fsimulator.scm.tap.subCluster.gain.set(gain = 1.0, mimoTap = repcap.MimoTap.Default, subCluster = repcap.SubCluster.Default) \n
		Queries the resulting relative gain of an enabled sub-cluster. \n
			:param gain: float Range: -50 to 0
			:param mimoTap: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tap')
			:param subCluster: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubCluster')
		"""
		param = Conversions.decimal_value_to_str(gain)
		mimoTap_cmd_val = self._cmd_group.get_repcap_cmd_value(mimoTap, repcap.MimoTap)
		subCluster_cmd_val = self._cmd_group.get_repcap_cmd_value(subCluster, repcap.SubCluster)
		self._core.io.write(f'SOURce<HwInstance>:FSIMulator:SCM:TAP{mimoTap_cmd_val}:SUBCluster{subCluster_cmd_val}:GAIN {param}')

	def get(self, mimoTap=repcap.MimoTap.Default, subCluster=repcap.SubCluster.Default) -> float:
		"""SCPI: [SOURce<HW>]:FSIMulator:SCM:TAP<ST>:SUBCluster<DI>:GAIN \n
		Snippet: value: float = driver.source.fsimulator.scm.tap.subCluster.gain.get(mimoTap = repcap.MimoTap.Default, subCluster = repcap.SubCluster.Default) \n
		Queries the resulting relative gain of an enabled sub-cluster. \n
			:param mimoTap: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tap')
			:param subCluster: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubCluster')
			:return: gain: float Range: -50 to 0"""
		mimoTap_cmd_val = self._cmd_group.get_repcap_cmd_value(mimoTap, repcap.MimoTap)
		subCluster_cmd_val = self._cmd_group.get_repcap_cmd_value(subCluster, repcap.SubCluster)
		response = self._core.io.query_str(f'SOURce<HwInstance>:FSIMulator:SCM:TAP{mimoTap_cmd_val}:SUBCluster{subCluster_cmd_val}:GAIN?')
		return Conversions.str_to_float(response)
