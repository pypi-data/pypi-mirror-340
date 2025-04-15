from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CatalogCls:
	"""Catalog commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("catalog", core, parent)

	def get(self, baseSt=repcap.BaseSt.Default) -> List[str]:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RTK:BASE<ST>:LOCation:CATalog \n
		Snippet: value: List[str] = driver.source.bb.gnss.rtk.base.location.catalog.get(baseSt = repcap.BaseSt.Default) \n
		Queries the names of predefined geographic locations of the RTK base station. The query returns a comma-separated list of
		available locations. For predefined geographic locations, see Table 'Coordinates of the simulated predefined positions'. \n
			:param baseSt: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Base')
			:return: gnss_location_names: No help available"""
		baseSt_cmd_val = self._cmd_group.get_repcap_cmd_value(baseSt, repcap.BaseSt)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RTK:BASE{baseSt_cmd_val}:LOCation:CATalog?')
		return Conversions.str_to_str_list(response)
