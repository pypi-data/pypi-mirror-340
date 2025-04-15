from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ConfigCls:
	"""Config commands group definition. 3 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("config", core, parent)

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .Catalog import CatalogCls
			self._catalog = CatalogCls(self._core, self._cmd_group)
		return self._catalog

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AutoManualMode:
		"""SCPI: [SOURce<HW>]:EFRontend:FREQuency:BAND:CONFig:MODE \n
		Snippet: value: enums.AutoManualMode = driver.source.efrontend.frequency.band.config.get_mode() \n
		Sets the mode for frequency band configuration of the external frontend. \n
			:return: mode: AUTO| MANual AUTO Configures the frequency band automatically. R&S FE44S and R&S FE50DTR: For bandwidths <= 400 MHz, 'IF Low' is used. For bandwidths larger than 400 MHz, 'IF High' is used. R&S FE170ST or R&S FE110ST: 'Spur Optimized' is used. MANual Uses the frequency band configured by [:SOURcehw]:EFRontend:FREQuency:BAND:CONFig:SELect.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:FREQuency:BAND:CONFig:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AutoManualMode)

	def set_mode(self, mode: enums.AutoManualMode) -> None:
		"""SCPI: [SOURce<HW>]:EFRontend:FREQuency:BAND:CONFig:MODE \n
		Snippet: driver.source.efrontend.frequency.band.config.set_mode(mode = enums.AutoManualMode.AUTO) \n
		Sets the mode for frequency band configuration of the external frontend. \n
			:param mode: AUTO| MANual AUTO Configures the frequency band automatically. R&S FE44S and R&S FE50DTR: For bandwidths <= 400 MHz, 'IF Low' is used. For bandwidths larger than 400 MHz, 'IF High' is used. R&S FE170ST or R&S FE110ST: 'Spur Optimized' is used. MANual Uses the frequency band configured by [:SOURcehw]:EFRontend:FREQuency:BAND:CONFig:SELect.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.AutoManualMode)
		self._core.io.write(f'SOURce<HwInstance>:EFRontend:FREQuency:BAND:CONFig:MODE {param}')

	def get_select(self) -> str:
		"""SCPI: [SOURce<HW>]:EFRontend:FREQuency:BAND:CONFig:SELect \n
		Snippet: value: str = driver.source.efrontend.frequency.band.config.get_select() \n
		Selects the frequency band configuration for the connected external frontend. Enter the mode as string, e.g. 'IF Low'. \n
			:return: sel_band_config: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:FREQuency:BAND:CONFig:SELect?')
		return trim_str_response(response)

	def set_select(self, sel_band_config: str) -> None:
		"""SCPI: [SOURce<HW>]:EFRontend:FREQuency:BAND:CONFig:SELect \n
		Snippet: driver.source.efrontend.frequency.band.config.set_select(sel_band_config = 'abc') \n
		Selects the frequency band configuration for the connected external frontend. Enter the mode as string, e.g. 'IF Low'. \n
			:param sel_band_config: string
		"""
		param = Conversions.value_to_quoted_str(sel_band_config)
		self._core.io.write(f'SOURce<HwInstance>:EFRontend:FREQuency:BAND:CONFig:SELect {param}')

	def clone(self) -> 'ConfigCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ConfigCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
