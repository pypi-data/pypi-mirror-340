from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.Utilities import trim_str_response
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SelectCls:
	"""Select commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("select", core, parent)

	def set(self, filename: str, baseband=repcap.Baseband.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:USER:[BB<ST>]:HOTime:FILE:[SELect] \n
		Snippet: driver.source.bb.esequencer.user.bb.hoTime.file.select.set(filename = 'abc', baseband = repcap.Baseband.Default) \n
		Selects an existing hopping list file. \n
			:param filename: string
			:param baseband: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bb')
		"""
		param = Conversions.value_to_quoted_str(filename)
		baseband_cmd_val = self._cmd_group.get_repcap_cmd_value(baseband, repcap.Baseband)
		self._core.io.write(f'SOURce<HwInstance>:BB:ESEQuencer:USER:BB{baseband_cmd_val}:HOTime:FILE:SELect {param}')

	def get(self, baseband=repcap.Baseband.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:ESEQuencer:USER:[BB<ST>]:HOTime:FILE:[SELect] \n
		Snippet: value: str = driver.source.bb.esequencer.user.bb.hoTime.file.select.get(baseband = repcap.Baseband.Default) \n
		Selects an existing hopping list file. \n
			:param baseband: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bb')
			:return: filename: string"""
		baseband_cmd_val = self._cmd_group.get_repcap_cmd_value(baseband, repcap.Baseband)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:ESEQuencer:USER:BB{baseband_cmd_val}:HOTime:FILE:SELect?')
		return trim_str_response(response)
