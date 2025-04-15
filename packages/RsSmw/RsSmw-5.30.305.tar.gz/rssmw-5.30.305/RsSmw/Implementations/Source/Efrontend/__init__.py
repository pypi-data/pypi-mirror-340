from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EfrontendCls:
	"""Efrontend commands group definition. 49 total commands, 13 Subgroups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("efrontend", core, parent)

	@property
	def alignment(self):
		"""alignment commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_alignment'):
			from .Alignment import AlignmentCls
			self._alignment = AlignmentCls(self._core, self._cmd_group)
		return self._alignment

	@property
	def cal(self):
		"""cal commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cal'):
			from .Cal import CalCls
			self._cal = CalCls(self._core, self._cmd_group)
		return self._cal

	@property
	def concurrent(self):
		"""concurrent commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_concurrent'):
			from .Concurrent import ConcurrentCls
			self._concurrent = ConcurrentCls(self._core, self._cmd_group)
		return self._concurrent

	@property
	def connection(self):
		"""connection commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_connection'):
			from .Connection import ConnectionCls
			self._connection = ConnectionCls(self._core, self._cmd_group)
		return self._connection

	@property
	def extDevice(self):
		"""extDevice commands group. 6 Sub-classes, 1 commands."""
		if not hasattr(self, '_extDevice'):
			from .ExtDevice import ExtDeviceCls
			self._extDevice = ExtDeviceCls(self._core, self._cmd_group)
		return self._extDevice

	@property
	def frequency(self):
		"""frequency commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def firmwareUpdate(self):
		"""firmwareUpdate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_firmwareUpdate'):
			from .FirmwareUpdate import FirmwareUpdateCls
			self._firmwareUpdate = FirmwareUpdateCls(self._core, self._cmd_group)
		return self._firmwareUpdate

	@property
	def loscillator(self):
		"""loscillator commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_loscillator'):
			from .Loscillator import LoscillatorCls
			self._loscillator = LoscillatorCls(self._core, self._cmd_group)
		return self._loscillator

	@property
	def network(self):
		"""network commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_network'):
			from .Network import NetworkCls
			self._network = NetworkCls(self._core, self._cmd_group)
		return self._network

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def screw(self):
		"""screw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_screw'):
			from .Screw import ScrewCls
			self._screw = ScrewCls(self._core, self._cmd_group)
		return self._screw

	@property
	def selftest(self):
		"""selftest commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_selftest'):
			from .Selftest import SelftestCls
			self._selftest = SelftestCls(self._core, self._cmd_group)
		return self._selftest

	@property
	def trxMode(self):
		"""trxMode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trxMode'):
			from .TrxMode import TrxModeCls
			self._trxMode = TrxModeCls(self._core, self._cmd_group)
		return self._trxMode

	# noinspection PyTypeChecker
	def get_amode(self) -> enums.EfePowAttMode:
		"""SCPI: [SOURce<HW>]:EFRontend:AMODe \n
		Snippet: value: enums.EfePowAttMode = driver.source.efrontend.get_amode() \n
		Sets the attenuator mode of the external frontend. \n
			:return: attenuation_mode: AUTO| MANual| AOFFset AUTO Sets the attenuation value automatically to the attenuation value provided from the connected external frontend. MANual Sets an attenuation value manually. AOFFset Requires frontend R&S FE170ST or R&S FE110ST. You can define an offset value which is added to the attenuation value provided from the connected external frontend.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:AMODe?')
		return Conversions.str_to_scalar_enum(response, enums.EfePowAttMode)

	def set_amode(self, attenuation_mode: enums.EfePowAttMode) -> None:
		"""SCPI: [SOURce<HW>]:EFRontend:AMODe \n
		Snippet: driver.source.efrontend.set_amode(attenuation_mode = enums.EfePowAttMode.AOFFset) \n
		Sets the attenuator mode of the external frontend. \n
			:param attenuation_mode: AUTO| MANual| AOFFset AUTO Sets the attenuation value automatically to the attenuation value provided from the connected external frontend. MANual Sets an attenuation value manually. AOFFset Requires frontend R&S FE170ST or R&S FE110ST. You can define an offset value which is added to the attenuation value provided from the connected external frontend.
		"""
		param = Conversions.enum_scalar_to_str(attenuation_mode, enums.EfePowAttMode)
		self._core.io.write(f'SOURce<HwInstance>:EFRontend:AMODe {param}')

	# noinspection PyTypeChecker
	def get_cmode(self) -> enums.ConMode:
		"""SCPI: [SOURce<HW>]:EFRontend:CMODe \n
		Snippet: value: enums.ConMode = driver.source.efrontend.get_cmode() \n
		Sets the mode of the SSL control connection between R&S SMW200A and external frontend. \n
			:return: fe_conn_mode: AUTO| LOCK| RXTX AUTO The R&S SMW200A locks external frontend, when activating the RF output at the R&S SMW200A (:OUTPut1 ON ) for output of the IF signal. The R&S SMW200A unlocks external frontend, when deactivating the RF output at the R&S SMW200A (:OUTPut1 OFF) . LOCK The external frontend is locked permanently. No other instrument can take over control. RXTX Requires an R&S FE50DTR connected to the R&S SMW200A. Connection mode for simultaneous Rx (receive) operation and Tx (transmit) operation of an R&S FE50DTR. Set this mode, if your test setup requires a release of connection lock. A connected vector signal analyzer can lock the external frontend for Rx operation.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:CMODe?')
		return Conversions.str_to_scalar_enum(response, enums.ConMode)

	def set_cmode(self, fe_conn_mode: enums.ConMode) -> None:
		"""SCPI: [SOURce<HW>]:EFRontend:CMODe \n
		Snippet: driver.source.efrontend.set_cmode(fe_conn_mode = enums.ConMode.AUTO) \n
		Sets the mode of the SSL control connection between R&S SMW200A and external frontend. \n
			:param fe_conn_mode: AUTO| LOCK| RXTX AUTO The R&S SMW200A locks external frontend, when activating the RF output at the R&S SMW200A (:OUTPut1 ON ) for output of the IF signal. The R&S SMW200A unlocks external frontend, when deactivating the RF output at the R&S SMW200A (:OUTPut1 OFF) . LOCK The external frontend is locked permanently. No other instrument can take over control. RXTX Requires an R&S FE50DTR connected to the R&S SMW200A. Connection mode for simultaneous Rx (receive) operation and Tx (transmit) operation of an R&S FE50DTR. Set this mode, if your test setup requires a release of connection lock. A connected vector signal analyzer can lock the external frontend for Rx operation.
		"""
		param = Conversions.enum_scalar_to_str(fe_conn_mode, enums.ConMode)
		self._core.io.write(f'SOURce<HwInstance>:EFRontend:CMODe {param}')

	def get_idn(self) -> str:
		"""SCPI: [SOURce<HW>]:EFRontend:IDN \n
		Snippet: value: str = driver.source.efrontend.get_idn() \n
		Identification Returns the IDN string, i.e. the identification of the external frontend. \n
			:return: idn_string: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:IDN?')
		return trim_str_response(response)

	def get_info(self) -> str:
		"""SCPI: [SOURce<HW>]:EFRontend:INFO \n
		Snippet: value: str = driver.source.efrontend.get_info() \n
		Queries information about the connected external frontend. \n
			:return: fe_info: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:INFO?')
		return trim_str_response(response)

	def get_ip_address(self) -> str:
		"""SCPI: [SOURce<HW>]:EFRontend:IPADdress \n
		Snippet: value: str = driver.source.efrontend.get_ip_address() \n
		Queries the IP address of the connected external frontend. \n
			:return: ip_address: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:IPADdress?')
		return trim_str_response(response)

	def get_list_py(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:EFRontend:LIST \n
		Snippet: value: List[str] = driver.source.efrontend.get_list_py() \n
		Queries connected external frontends in a comma-separated list. \n
			:return: filter_py: String
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:LIST?')
		return Conversions.str_to_str_list(response)

	def get_opt(self) -> str:
		"""SCPI: [SOURce<HW>]:EFRontend:OPT \n
		Snippet: value: str = driver.source.efrontend.get_opt() \n
		Option identification query Queries the options included in the external frontend. For more information, refer to the
		specifications document. \n
			:return: opt_string: string The query returns a list of options. The options are returned at fixed positions in a comma-separated string. A zero is returned for options that are not installed.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:OPT?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	def get_rf_connector(self) -> enums.FenUmbRfCon:
		"""SCPI: [SOURce<HW>]:EFRontend:RFConnector \n
		Snippet: value: enums.FenUmbRfCon = driver.source.efrontend.get_rf_connector() \n
		Queries the active RF output connector at the connected RF frontend. \n
			:return: fe_output_path: NONE| RFA| RFB NONE No frontend connected. RFA Output connector 'RF A' is active at the external frontend. RFB Output connector 'RF B' is active at the external frontend.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:RFConnector?')
		return Conversions.str_to_scalar_enum(response, enums.FenUmbRfCon)

	def set_rf_connector(self, fe_output_path: enums.FenUmbRfCon) -> None:
		"""SCPI: [SOURce<HW>]:EFRontend:RFConnector \n
		Snippet: driver.source.efrontend.set_rf_connector(fe_output_path = enums.FenUmbRfCon.NONE) \n
		Queries the active RF output connector at the connected RF frontend. \n
			:param fe_output_path: NONE| RFA| RFB NONE No frontend connected. RFA Output connector 'RF A' is active at the external frontend. RFB Output connector 'RF B' is active at the external frontend.
		"""
		param = Conversions.enum_scalar_to_str(fe_output_path, enums.FenUmbRfCon)
		self._core.io.write(f'SOURce<HwInstance>:EFRontend:RFConnector {param}')

	def clone(self) -> 'EfrontendCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EfrontendCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
