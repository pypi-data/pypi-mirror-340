from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CtypeCls:
	"""Ctype commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ctype", core, parent)

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.BtoChnnelTypeData:
		"""SCPI: [SOURce<HW>]:BB:BTOoth:ECONfiguration:DCTable:SET<CH>:CTYPe \n
		Snippet: value: enums.BtoChnnelTypeData = driver.source.bb.btooth.econfiguration.dcTable.set.ctype.get(channel = repcap.Channel.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Set')
			:return: channel_type: No help available"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:DCTable:SET{channel_cmd_val}:CTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoChnnelTypeData)
