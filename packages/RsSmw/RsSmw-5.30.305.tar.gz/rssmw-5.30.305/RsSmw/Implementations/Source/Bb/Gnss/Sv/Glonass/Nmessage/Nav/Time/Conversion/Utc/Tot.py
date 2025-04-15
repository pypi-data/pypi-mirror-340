from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TotCls:
	"""Tot commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tot", core, parent)

	def get_unscaled(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:GLONass:NMESsage:NAV:TIME:CONVersion:UTC:TOT:UNSCaled \n
		Snippet: value: int = driver.source.bb.gnss.sv.glonass.nmessage.nav.time.conversion.utc.tot.get_unscaled() \n
		No command help available \n
			:return: tot: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:SV:GLONass:NMESsage:NAV:TIME:CONVersion:UTC:TOT:UNSCaled?')
		return Conversions.str_to_int(response)

	def set_unscaled(self, tot: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:GLONass:NMESsage:NAV:TIME:CONVersion:UTC:TOT:UNSCaled \n
		Snippet: driver.source.bb.gnss.sv.glonass.nmessage.nav.time.conversion.utc.tot.set_unscaled(tot = 1) \n
		No command help available \n
			:param tot: No help available
		"""
		param = Conversions.decimal_value_to_str(tot)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:GLONass:NMESsage:NAV:TIME:CONVersion:UTC:TOT:UNSCaled {param}')

	def get_value(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:GLONass:NMESsage:NAV:TIME:CONVersion:UTC:TOT \n
		Snippet: value: int = driver.source.bb.gnss.sv.glonass.nmessage.nav.time.conversion.utc.tot.get_value() \n
		No command help available \n
			:return: tot: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:SV:GLONass:NMESsage:NAV:TIME:CONVersion:UTC:TOT?')
		return Conversions.str_to_int(response)

	def set_value(self, tot: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:SV:GLONass:NMESsage:NAV:TIME:CONVersion:UTC:TOT \n
		Snippet: driver.source.bb.gnss.sv.glonass.nmessage.nav.time.conversion.utc.tot.set_value(tot = 1) \n
		No command help available \n
			:param tot: No help available
		"""
		param = Conversions.decimal_value_to_str(tot)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:GLONass:NMESsage:NAV:TIME:CONVersion:UTC:TOT {param}')
