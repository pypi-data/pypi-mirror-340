from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Types import DataType
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UserCls:
	"""User commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("user", core, parent)

	def get(self, cat_dir: str = None) -> List[str]:
		"""SCPI: [SOURce<HW>]:CEMulation:MIMO:ANTenna:PATTern:CATalog:USER \n
		Snippet: value: List[str] = driver.source.cemulation.mimo.antenna.pattern.catalog.user.get(cat_dir = 'abc') \n
		No command help available \n
			:param cat_dir: No help available
			:return: catalog: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('cat_dir', cat_dir, DataType.String, None, is_optional=True))
		response = self._core.io.query_str(f'SOURce<HwInstance>:CEMulation:MIMO:ANTenna:PATTern:CATalog:USER? {param}'.rstrip())
		return Conversions.str_to_str_list(response)
