from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SvidCls:
	"""Svid commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("svid", core, parent)

	def set(self, svid: float, vdbTransmitter=repcap.VdbTransmitter.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:SVID \n
		Snippet: driver.source.bb.gbas.vdb.mconfig.svid.set(svid = 1.0, vdbTransmitter = repcap.VdbTransmitter.Default) \n
		Sets the standard deviation of a normal distribution connected to the residual ionospheric uncertainty which is caused by
		spatial decorrelation. \n
			:param svid: float Range: 0 to 2.55e-05
			:param vdbTransmitter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
		"""
		param = Conversions.decimal_value_to_str(svid)
		vdbTransmitter_cmd_val = self._cmd_group.get_repcap_cmd_value(vdbTransmitter, repcap.VdbTransmitter)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{vdbTransmitter_cmd_val}:MCONfig:SVID {param}')

	def get(self, vdbTransmitter=repcap.VdbTransmitter.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:SVID \n
		Snippet: value: float = driver.source.bb.gbas.vdb.mconfig.svid.get(vdbTransmitter = repcap.VdbTransmitter.Default) \n
		Sets the standard deviation of a normal distribution connected to the residual ionospheric uncertainty which is caused by
		spatial decorrelation. \n
			:param vdbTransmitter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: svid: float Range: 0 to 2.55e-05"""
		vdbTransmitter_cmd_val = self._cmd_group.get_repcap_cmd_value(vdbTransmitter, repcap.VdbTransmitter)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{vdbTransmitter_cmd_val}:MCONfig:SVID?')
		return Conversions.str_to_float(response)
