from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Utilities import trim_str_response
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MountpointCls:
	"""Mountpoint commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mountpoint", core, parent)

	def get(self, baseSt=repcap.BaseSt.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:GNSS:RTK:BASE<ST>:MOUNtpoint \n
		Snippet: value: str = driver.source.bb.gnss.rtk.base.mountpoint.get(baseSt = repcap.BaseSt.Default) \n
		Sets the mountpoint for RTK simulation. \n
			:param baseSt: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Base')
			:return: mountpoint: string"""
		baseSt_cmd_val = self._cmd_group.get_repcap_cmd_value(baseSt, repcap.BaseSt)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RTK:BASE{baseSt_cmd_val}:MOUNtpoint?')
		return trim_str_response(response)
