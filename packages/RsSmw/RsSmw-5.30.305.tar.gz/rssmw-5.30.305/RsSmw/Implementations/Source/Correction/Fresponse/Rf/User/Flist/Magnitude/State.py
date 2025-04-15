from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, freq_corr_rf_mag_st: bool, index=repcap.Index.Default) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:USER:FLISt<CH>:MAGNitude:[STATe] \n
		Snippet: driver.source.correction.fresponse.rf.user.flist.magnitude.state.set(freq_corr_rf_mag_st = False, index = repcap.Index.Default) \n
		Deletes all entries in the list. \n
			:param freq_corr_rf_mag_st: No help available
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Flist')
		"""
		param = Conversions.bool_to_str(freq_corr_rf_mag_st)
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:RF:USER:FLISt{index_cmd_val}:MAGNitude:STATe {param}')

	def get(self, index=repcap.Index.Default) -> bool:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:USER:FLISt<CH>:MAGNitude:[STATe] \n
		Snippet: value: bool = driver.source.correction.fresponse.rf.user.flist.magnitude.state.get(index = repcap.Index.Default) \n
		Deletes all entries in the list. \n
			:param index: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Flist')
			:return: freq_corr_rf_mag_st: No help available"""
		index_cmd_val = self._cmd_group.get_repcap_cmd_value(index, repcap.Index)
		response = self._core.io.query_str(f'SOURce<HwInstance>:CORRection:FRESponse:RF:USER:FLISt{index_cmd_val}:MAGNitude:STATe?')
		return Conversions.str_to_bool(response)
