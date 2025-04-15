from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpreadCls:
	"""Spread commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("spread", core, parent)

	def set(self, spread: float, cluster=repcap.Cluster.Default) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:MIMO:SCWI:CLUSter<CH>:DEParture:SPRead \n
		Snippet: driver.source.cemulation.mimo.scwi.cluster.departure.spread.set(spread = 1.0, cluster = repcap.Cluster.Default) \n
		No command help available \n
			:param spread: No help available
			:param cluster: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cluster')
		"""
		param = Conversions.decimal_value_to_str(spread)
		cluster_cmd_val = self._cmd_group.get_repcap_cmd_value(cluster, repcap.Cluster)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:MIMO:SCWI:CLUSter{cluster_cmd_val}:DEParture:SPRead {param}')

	def get(self, cluster=repcap.Cluster.Default) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:MIMO:SCWI:CLUSter<CH>:DEParture:SPRead \n
		Snippet: value: float = driver.source.cemulation.mimo.scwi.cluster.departure.spread.get(cluster = repcap.Cluster.Default) \n
		No command help available \n
			:param cluster: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cluster')
			:return: spread: No help available"""
		cluster_cmd_val = self._cmd_group.get_repcap_cmd_value(cluster, repcap.Cluster)
		response = self._core.io.query_str(f'SOURce<HwInstance>:CEMulation:MIMO:SCWI:CLUSter{cluster_cmd_val}:DEParture:SPRead?')
		return Conversions.str_to_float(response)
