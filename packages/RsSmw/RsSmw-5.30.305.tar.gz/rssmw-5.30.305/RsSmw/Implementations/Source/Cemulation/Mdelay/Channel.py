from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ChannelCls:
	"""Channel commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("channel", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.FadMpRopChanMode:
		"""SCPI: [SOURce<HW>]:CEMulation:MDELay:CHANnel:MODE \n
		Snippet: value: enums.FadMpRopChanMode = driver.source.cemulation.mdelay.channel.get_mode() \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CEMulation:MDELay:CHANnel:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FadMpRopChanMode)

	def set_mode(self, mode: enums.FadMpRopChanMode) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:MDELay:CHANnel:MODE \n
		Snippet: driver.source.cemulation.mdelay.channel.set_mode(mode = enums.FadMpRopChanMode.ALL) \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.FadMpRopChanMode)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:MDELay:CHANnel:MODE {param}')
