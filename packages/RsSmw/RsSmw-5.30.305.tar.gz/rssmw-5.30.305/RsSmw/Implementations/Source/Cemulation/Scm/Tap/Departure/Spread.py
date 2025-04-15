from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpreadCls:
	"""Spread commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("spread", core, parent)

	def set(self, spread: float, mimoTap=repcap.MimoTap.Default) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:TAP<ST>:DEParture:SPRead \n
		Snippet: driver.source.cemulation.scm.tap.departure.spread.set(spread = 1.0, mimoTap = repcap.MimoTap.Default) \n
		No command help available \n
			:param spread: No help available
			:param mimoTap: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tap')
		"""
		param = Conversions.decimal_value_to_str(spread)
		mimoTap_cmd_val = self._cmd_group.get_repcap_cmd_value(mimoTap, repcap.MimoTap)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:SCM:TAP{mimoTap_cmd_val}:DEParture:SPRead {param}')

	def get(self, mimoTap=repcap.MimoTap.Default) -> float:
		"""SCPI: [SOURce<HW>]:CEMulation:SCM:TAP<ST>:DEParture:SPRead \n
		Snippet: value: float = driver.source.cemulation.scm.tap.departure.spread.get(mimoTap = repcap.MimoTap.Default) \n
		No command help available \n
			:param mimoTap: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tap')
			:return: spread: No help available"""
		mimoTap_cmd_val = self._cmd_group.get_repcap_cmd_value(mimoTap, repcap.MimoTap)
		response = self._core.io.query_str(f'SOURce<HwInstance>:CEMulation:SCM:TAP{mimoTap_cmd_val}:DEParture:SPRead?')
		return Conversions.str_to_float(response)
