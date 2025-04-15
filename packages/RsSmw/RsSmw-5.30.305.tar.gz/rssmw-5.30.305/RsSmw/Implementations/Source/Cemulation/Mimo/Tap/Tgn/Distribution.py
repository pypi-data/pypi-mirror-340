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

	def set(self, distribution: enums.FadMimoScmDist, mimoTap=repcap.MimoTap.Default) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:MIMO:TAP<CH>:TGN:DISTribution \n
		Snippet: driver.source.cemulation.mimo.tap.tgn.distribution.set(distribution = enums.FadMimoScmDist.EQUal, mimoTap = repcap.MimoTap.Default) \n
		No command help available \n
			:param distribution: No help available
			:param mimoTap: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tap')
		"""
		param = Conversions.enum_scalar_to_str(distribution, enums.FadMimoScmDist)
		mimoTap_cmd_val = self._cmd_group.get_repcap_cmd_value(mimoTap, repcap.MimoTap)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:MIMO:TAP{mimoTap_cmd_val}:TGN:DISTribution {param}')

	# noinspection PyTypeChecker
	def get(self, mimoTap=repcap.MimoTap.Default) -> enums.FadMimoScmDist:
		"""SCPI: [SOURce<HW>]:CEMulation:MIMO:TAP<CH>:TGN:DISTribution \n
		Snippet: value: enums.FadMimoScmDist = driver.source.cemulation.mimo.tap.tgn.distribution.get(mimoTap = repcap.MimoTap.Default) \n
		No command help available \n
			:param mimoTap: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tap')
			:return: distribution: No help available"""
		mimoTap_cmd_val = self._cmd_group.get_repcap_cmd_value(mimoTap, repcap.MimoTap)
		response = self._core.io.query_str(f'SOURce<HwInstance>:CEMulation:MIMO:TAP{mimoTap_cmd_val}:TGN:DISTribution?')
		return Conversions.str_to_scalar_enum(response, enums.FadMimoScmDist)
