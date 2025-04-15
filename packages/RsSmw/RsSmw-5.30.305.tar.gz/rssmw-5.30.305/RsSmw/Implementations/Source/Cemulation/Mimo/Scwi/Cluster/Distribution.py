from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DistributionCls:
	"""Distribution commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("distribution", core, parent)

	def set(self, distribution: enums.FadMimoScmDist, cluster=repcap.Cluster.Default) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:MIMO:SCWI:CLUSter<CH>:DISTribution \n
		Snippet: driver.source.cemulation.mimo.scwi.cluster.distribution.set(distribution = enums.FadMimoScmDist.EQUal, cluster = repcap.Cluster.Default) \n
		No command help available \n
			:param distribution: No help available
			:param cluster: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cluster')
		"""
		param = Conversions.enum_scalar_to_str(distribution, enums.FadMimoScmDist)
		cluster_cmd_val = self._cmd_group.get_repcap_cmd_value(cluster, repcap.Cluster)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:MIMO:SCWI:CLUSter{cluster_cmd_val}:DISTribution {param}')

	# noinspection PyTypeChecker
	def get(self, cluster=repcap.Cluster.Default) -> enums.FadMimoScmDist:
		"""SCPI: [SOURce<HW>]:CEMulation:MIMO:SCWI:CLUSter<CH>:DISTribution \n
		Snippet: value: enums.FadMimoScmDist = driver.source.cemulation.mimo.scwi.cluster.distribution.get(cluster = repcap.Cluster.Default) \n
		No command help available \n
			:param cluster: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cluster')
			:return: distribution: No help available"""
		cluster_cmd_val = self._cmd_group.get_repcap_cmd_value(cluster, repcap.Cluster)
		response = self._core.io.query_str(f'SOURce<HwInstance>:CEMulation:MIMO:SCWI:CLUSter{cluster_cmd_val}:DISTribution?')
		return Conversions.str_to_scalar_enum(response, enums.FadMimoScmDist)
