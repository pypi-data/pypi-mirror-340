from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ObjectCls:
	"""Object commands group definition. 30 total commands, 15 Subgroups, 2 group commands
	Repeated Capability: ObjectIx, default value after init: ObjectIx.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("object", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_objectIx_get', 'repcap_objectIx_set', repcap.ObjectIx.Nr1)

	def repcap_objectIx_set(self, objectIx: repcap.ObjectIx) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to ObjectIx.Default.
		Default value after init: ObjectIx.Nr1"""
		self._cmd_group.set_repcap_enum_value(objectIx)

	def repcap_objectIx_get(self) -> repcap.ObjectIx:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def copy(self):
		"""copy commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_copy'):
			from .Copy import CopyCls
			self._copy = CopyCls(self._core, self._cmd_group)
		return self._copy

	@property
	def direction(self):
		"""direction commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_direction'):
			from .Direction import DirectionCls
			self._direction = DirectionCls(self._core, self._cmd_group)
		return self._direction

	@property
	def fepNumber(self):
		"""fepNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fepNumber'):
			from .FepNumber import FepNumberCls
			self._fepNumber = FepNumberCls(self._core, self._cmd_group)
		return self._fepNumber

	@property
	def hold(self):
		"""hold commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_hold'):
			from .Hold import HoldCls
			self._hold = HoldCls(self._core, self._cmd_group)
		return self._hold

	@property
	def name(self):
		"""name commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_name'):
			from .Name import NameCls
			self._name = NameCls(self._core, self._cmd_group)
		return self._name

	@property
	def ovelocity(self):
		"""ovelocity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ovelocity'):
			from .Ovelocity import OvelocityCls
			self._ovelocity = OvelocityCls(self._core, self._cmd_group)
		return self._ovelocity

	@property
	def phase(self):
		"""phase commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_phase'):
			from .Phase import PhaseCls
			self._phase = PhaseCls(self._core, self._cmd_group)
		return self._phase

	@property
	def power(self):
		"""power commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def range(self):
		"""range commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_range'):
			from .Range import RangeCls
			self._range = RangeCls(self._core, self._cmd_group)
		return self._range

	@property
	def rcs(self):
		"""rcs commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_rcs'):
			from .Rcs import RcsCls
			self._rcs = RcsCls(self._core, self._cmd_group)
		return self._rcs

	@property
	def simMode(self):
		"""simMode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_simMode'):
			from .SimMode import SimModeCls
			self._simMode = SimModeCls(self._core, self._cmd_group)
		return self._simMode

	@property
	def store(self):
		"""store commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_store'):
			from .Store import StoreCls
			self._store = StoreCls(self._core, self._cmd_group)
		return self._store

	@property
	def time(self):
		"""time commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_time'):
			from .Time import TimeCls
			self._time = TimeCls(self._core, self._cmd_group)
		return self._time

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	@property
	def ulist(self):
		"""ulist commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_ulist'):
			from .Ulist import UlistCls
			self._ulist = UlistCls(self._core, self._cmd_group)
		return self._ulist

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:REGenerator:OBJect:CATalog \n
		Snippet: value: List[str] = driver.source.regenerator.object.get_catalog() \n
		Queries files with object setting in the default directory. Listed are files with the file extension *.reg_obj. Refer to
		'Accessing Files in the Default or Specified Directory' for general information on file handling in the default and in a
		specific directory. \n
			:return: filenames: filename1,filename2,... Returns a string of file names separated by commas.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:REGenerator:OBJect:CATalog?')
		return Conversions.str_to_str_list(response)

	def load(self, filename: str, objectIx=repcap.ObjectIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:REGenerator:OBJect<CH>:LOAD \n
		Snippet: driver.source.regenerator.object.load(filename = 'abc', objectIx = repcap.ObjectIx.Default) \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.reg_obj. Refer to
		'Accessing Files in the Default or Specified Directory' for general information on file handling in the default and in a
		specific directory. \n
			:param filename: string
			:param objectIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Object')
		"""
		param = Conversions.value_to_quoted_str(filename)
		objectIx_cmd_val = self._cmd_group.get_repcap_cmd_value(objectIx, repcap.ObjectIx)
		self._core.io.write(f'SOURce<HwInstance>:REGenerator:OBJect{objectIx_cmd_val}:LOAD {param}')

	def clone(self) -> 'ObjectCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ObjectCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
