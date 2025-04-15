from enum import Enum
# noinspection PyPep8Naming
from .Internal.RepeatedCapability import VALUE_DEFAULT as DefaultRepCap
# noinspection PyPep8Naming
from .Internal.RepeatedCapability import VALUE_EMPTY as EmptyRepCap
# noinspection PyPep8Naming,PyUnresolvedReferences
from .Internal.RepeatedCapability import VALUE_SKIP_HEADER as SkipHeaderRepCap


# noinspection SpellCheckingInspection
class HwInstance(Enum):
	"""Global Repeated capability HwInstance"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	InstA = 1
	InstB = 2
	InstC = 3
	InstD = 4
	InstE = 5
	InstF = 6
	InstG = 7
	InstH = 8


# noinspection SpellCheckingInspection
class AccessPointNull(Enum):
	"""Repeated capability AccessPointNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1000 = 1000
	Nr2000 = 2000
	Nr3000 = 3000
	Nr4000 = 4000
	Nr5000 = 5000
	Nr6000 = 6000
	Nr7000 = 7000


# noinspection SpellCheckingInspection
class AddressField(Enum):
	"""Repeated capability AddressField"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4


# noinspection SpellCheckingInspection
class AiOrder(Enum):
	"""Repeated capability AiOrder"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3


# noinspection SpellCheckingInspection
class AllocationNull(Enum):
	"""Repeated capability AllocationNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63


# noinspection SpellCheckingInspection
class AlphaNull(Enum):
	"""Repeated capability AlphaNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3


# noinspection SpellCheckingInspection
class Antenna(Enum):
	"""Repeated capability Antenna"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4


# noinspection SpellCheckingInspection
class AntennaPattern(Enum):
	"""Repeated capability AntennaPattern"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16


# noinspection SpellCheckingInspection
class AntennaPortIx(Enum):
	"""Repeated capability AntennaPortIx"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1


# noinspection SpellCheckingInspection
class AntennaPortNull(Enum):
	"""Repeated capability AntennaPortNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63
	Nr64 = 64
	Nr2000 = 2000
	Nr2001 = 2001


# noinspection SpellCheckingInspection
class AttenuationList(Enum):
	"""Repeated capability AttenuationList"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16


# noinspection SpellCheckingInspection
class AttenuationNull(Enum):
	"""Repeated capability AttenuationNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40


# noinspection SpellCheckingInspection
class Band(Enum):
	"""Repeated capability Band"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8


# noinspection SpellCheckingInspection
class Baseband(Enum):
	"""Repeated capability Baseband"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4


# noinspection SpellCheckingInspection
class BasebandNull(Enum):
	"""Repeated capability BasebandNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3


# noinspection SpellCheckingInspection
class BaseSt(Enum):
	"""Repeated capability BaseSt"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16


# noinspection SpellCheckingInspection
class BaseStation(Enum):
	"""Repeated capability BaseStation"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4


# noinspection SpellCheckingInspection
class BetaNull(Enum):
	"""Repeated capability BetaNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3


# noinspection SpellCheckingInspection
class BitNumberNull(Enum):
	"""Repeated capability BitNumberNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15


# noinspection SpellCheckingInspection
class BurstNull(Enum):
	"""Repeated capability BurstNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63


# noinspection SpellCheckingInspection
class BwPartNull(Enum):
	"""Repeated capability BwPartNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31


# noinspection SpellCheckingInspection
class Carrier(Enum):
	"""Repeated capability Carrier"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63
	Nr64 = 64


# noinspection SpellCheckingInspection
class CarrierNull(Enum):
	"""Repeated capability CarrierNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63


# noinspection SpellCheckingInspection
class CeLevel(Enum):
	"""Repeated capability CeLevel"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3


# noinspection SpellCheckingInspection
class Cell(Enum):
	"""Repeated capability Cell"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63
	Nr64 = 64


# noinspection SpellCheckingInspection
class CellNull(Enum):
	"""Repeated capability CellNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63


# noinspection SpellCheckingInspection
class Channel(Enum):
	"""Repeated capability Channel"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63
	Nr64 = 64


# noinspection SpellCheckingInspection
class ChannelNull(Enum):
	"""Repeated capability ChannelNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63


# noinspection SpellCheckingInspection
class ChannelQualId(Enum):
	"""Repeated capability ChannelQualId"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16


# noinspection SpellCheckingInspection
class Cluster(Enum):
	"""Repeated capability Cluster"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20


# noinspection SpellCheckingInspection
class Codeword(Enum):
	"""Repeated capability Codeword"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16


# noinspection SpellCheckingInspection
class CodewordNull(Enum):
	"""Repeated capability CodewordNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15


# noinspection SpellCheckingInspection
class Column(Enum):
	"""Repeated capability Column"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32


# noinspection SpellCheckingInspection
class ColumnNull(Enum):
	"""Repeated capability ColumnNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31


# noinspection SpellCheckingInspection
class CommandBlock(Enum):
	"""Repeated capability CommandBlock"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63
	Nr64 = 64
	Nr65 = 65
	Nr66 = 66
	Nr67 = 67
	Nr68 = 68
	Nr69 = 69
	Nr70 = 70
	Nr71 = 71
	Nr72 = 72
	Nr73 = 73
	Nr74 = 74
	Nr75 = 75
	Nr76 = 76
	Nr77 = 77
	Nr78 = 78
	Nr79 = 79
	Nr80 = 80
	Nr81 = 81
	Nr82 = 82
	Nr83 = 83
	Nr84 = 84
	Nr85 = 85
	Nr86 = 86
	Nr87 = 87
	Nr88 = 88
	Nr89 = 89
	Nr90 = 90
	Nr91 = 91
	Nr92 = 92
	Nr93 = 93
	Nr94 = 94
	Nr95 = 95
	Nr96 = 96
	Nr97 = 97
	Nr98 = 98
	Nr99 = 99
	Nr100 = 100


# noinspection SpellCheckingInspection
class ConfigurationNull(Enum):
	"""Repeated capability ConfigurationNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15


# noinspection SpellCheckingInspection
class ConstelationPointNull(Enum):
	"""Repeated capability ConstelationPointNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32


# noinspection SpellCheckingInspection
class CoresetLength(Enum):
	"""Repeated capability CoresetLength"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16


# noinspection SpellCheckingInspection
class CsiRefSignal(Enum):
	"""Repeated capability CsiRefSignal"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5


# noinspection SpellCheckingInspection
class DeselectAll(Enum):
	"""Repeated capability DeselectAll"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7


# noinspection SpellCheckingInspection
class DigitalIq(Enum):
	"""Repeated capability DigitalIq"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4


# noinspection SpellCheckingInspection
class Echo(Enum):
	"""Repeated capability Echo"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9


# noinspection SpellCheckingInspection
class ErrorCount(Enum):
	"""Repeated capability ErrorCount"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16


# noinspection SpellCheckingInspection
class External(Enum):
	"""Repeated capability External"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4


# noinspection SpellCheckingInspection
class ExternalDevice(Enum):
	"""Repeated capability ExternalDevice"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8


# noinspection SpellCheckingInspection
class FadingGroup(Enum):
	"""Repeated capability FadingGroup"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4


# noinspection SpellCheckingInspection
class FdbTransmitter(Enum):
	"""Repeated capability FdbTransmitter"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8


# noinspection SpellCheckingInspection
class FmBlock(Enum):
	"""Repeated capability FmBlock"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63
	Nr64 = 64


# noinspection SpellCheckingInspection
class FrameBlock(Enum):
	"""Repeated capability FrameBlock"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63
	Nr64 = 64
	Nr65 = 65
	Nr66 = 66
	Nr67 = 67
	Nr68 = 68
	Nr69 = 69
	Nr70 = 70
	Nr71 = 71
	Nr72 = 72
	Nr73 = 73
	Nr74 = 74
	Nr75 = 75
	Nr76 = 76
	Nr77 = 77
	Nr78 = 78
	Nr79 = 79
	Nr80 = 80
	Nr81 = 81
	Nr82 = 82
	Nr83 = 83
	Nr84 = 84
	Nr85 = 85
	Nr86 = 86
	Nr87 = 87
	Nr88 = 88
	Nr89 = 89
	Nr90 = 90
	Nr91 = 91
	Nr92 = 92
	Nr93 = 93
	Nr94 = 94
	Nr95 = 95
	Nr96 = 96
	Nr97 = 97
	Nr98 = 98
	Nr99 = 99
	Nr100 = 100


# noinspection SpellCheckingInspection
class FrameIx(Enum):
	"""Repeated capability FrameIx"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2


# noinspection SpellCheckingInspection
class FrCfgIxNull(Enum):
	"""Repeated capability FrCfgIxNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31


# noinspection SpellCheckingInspection
class GainVector(Enum):
	"""Repeated capability GainVector"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8


# noinspection SpellCheckingInspection
class GeneratorIx(Enum):
	"""Repeated capability GeneratorIx"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8


# noinspection SpellCheckingInspection
class GnssPsRandomNumberNull(Enum):
	"""Repeated capability GnssPsRandomNumberNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr120 = 120
	Nr122 = 122
	Nr124 = 124
	Nr126 = 126
	Nr127 = 127
	Nr128 = 128
	Nr129 = 129
	Nr131 = 131
	Nr133 = 133
	Nr134 = 134
	Nr135 = 135
	Nr136 = 136
	Nr137 = 137
	Nr138 = 138


# noinspection SpellCheckingInspection
class GroupNull(Enum):
	"""Repeated capability GroupNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15


# noinspection SpellCheckingInspection
class Index(Enum):
	"""Repeated capability Index"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63
	Nr64 = 64


# noinspection SpellCheckingInspection
class IndexNull(Enum):
	"""Repeated capability IndexNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63


# noinspection SpellCheckingInspection
class InputIx(Enum):
	"""Repeated capability InputIx"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8


# noinspection SpellCheckingInspection
class InterlaceNull(Enum):
	"""Repeated capability InterlaceNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9


# noinspection SpellCheckingInspection
class IqConnector(Enum):
	"""Repeated capability IqConnector"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4


# noinspection SpellCheckingInspection
class ItemNull(Enum):
	"""Repeated capability ItemNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63


# noinspection SpellCheckingInspection
class LayerNull(Enum):
	"""Repeated capability LayerNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7


# noinspection SpellCheckingInspection
class Level(Enum):
	"""Repeated capability Level"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16


# noinspection SpellCheckingInspection
class LfOutput(Enum):
	"""Repeated capability LfOutput"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4


# noinspection SpellCheckingInspection
class ListIndexNull(Enum):
	"""Repeated capability ListIndexNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16


# noinspection SpellCheckingInspection
class MacPdu(Enum):
	"""Repeated capability MacPdu"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63
	Nr64 = 64


# noinspection SpellCheckingInspection
class MimoTap(Enum):
	"""Repeated capability MimoTap"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10


# noinspection SpellCheckingInspection
class MobileStation(Enum):
	"""Repeated capability MobileStation"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4


# noinspection SpellCheckingInspection
class ModCodSet(Enum):
	"""Repeated capability ModCodSet"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63
	Nr64 = 64
	Nr65 = 65
	Nr66 = 66
	Nr67 = 67
	Nr68 = 68
	Nr69 = 69
	Nr70 = 70
	Nr71 = 71
	Nr72 = 72
	Nr73 = 73
	Nr74 = 74
	Nr75 = 75
	Nr76 = 76
	Nr77 = 77
	Nr78 = 78
	Nr79 = 79
	Nr80 = 80
	Nr81 = 81
	Nr82 = 82
	Nr83 = 83
	Nr84 = 84
	Nr85 = 85
	Nr86 = 86
	Nr87 = 87
	Nr88 = 88
	Nr89 = 89
	Nr90 = 90
	Nr91 = 91
	Nr92 = 92
	Nr93 = 93
	Nr94 = 94
	Nr95 = 95
	Nr96 = 96
	Nr97 = 97
	Nr98 = 98
	Nr99 = 99
	Nr100 = 100


# noinspection SpellCheckingInspection
class MonitorPane(Enum):
	"""Repeated capability MonitorPane"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2


# noinspection SpellCheckingInspection
class NoisePoint(Enum):
	"""Repeated capability NoisePoint"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5


# noinspection SpellCheckingInspection
class NotchFilter(Enum):
	"""Repeated capability NotchFilter"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8


# noinspection SpellCheckingInspection
class ObjectIx(Enum):
	"""Repeated capability ObjectIx"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12


# noinspection SpellCheckingInspection
class ObscuredArea(Enum):
	"""Repeated capability ObscuredArea"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16


# noinspection SpellCheckingInspection
class Offset(Enum):
	"""Repeated capability Offset"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63
	Nr64 = 64


# noinspection SpellCheckingInspection
class OffsetNull(Enum):
	"""Repeated capability OffsetNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63


# noinspection SpellCheckingInspection
class Output(Enum):
	"""Repeated capability Output"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63
	Nr64 = 64


# noinspection SpellCheckingInspection
class Packet(Enum):
	"""Repeated capability Packet"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32


# noinspection SpellCheckingInspection
class Path(Enum):
	"""Repeated capability Path"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8


# noinspection SpellCheckingInspection
class PatternIx(Enum):
	"""Repeated capability PatternIx"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16


# noinspection SpellCheckingInspection
class PatternNull(Enum):
	"""Repeated capability PatternNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15


# noinspection SpellCheckingInspection
class Port(Enum):
	"""Repeated capability Port"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8


# noinspection SpellCheckingInspection
class PortNull(Enum):
	"""Repeated capability PortNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7


# noinspection SpellCheckingInspection
class RateSettingNull(Enum):
	"""Repeated capability RateSettingNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32


# noinspection SpellCheckingInspection
class Ray(Enum):
	"""Repeated capability Ray"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6


# noinspection SpellCheckingInspection
class Region(Enum):
	"""Repeated capability Region"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5


# noinspection SpellCheckingInspection
class ResourceNull(Enum):
	"""Repeated capability ResourceNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63


# noinspection SpellCheckingInspection
class ResourceSetNull(Enum):
	"""Repeated capability ResourceSetNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15


# noinspection SpellCheckingInspection
class Row(Enum):
	"""Repeated capability Row"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32


# noinspection SpellCheckingInspection
class RowNull(Enum):
	"""Repeated capability RowNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31


# noinspection SpellCheckingInspection
class SatelliteSvid(Enum):
	"""Repeated capability SatelliteSvid"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr193 = 193
	Nr194 = 194
	Nr195 = 195


# noinspection SpellCheckingInspection
class SelectAllNull(Enum):
	"""Repeated capability SelectAllNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7


# noinspection SpellCheckingInspection
class Sequencer(Enum):
	"""Repeated capability Sequencer"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6


# noinspection SpellCheckingInspection
class ServiceListTable(Enum):
	"""Repeated capability ServiceListTable"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63
	Nr64 = 64
	Nr65 = 65
	Nr66 = 66
	Nr67 = 67
	Nr68 = 68
	Nr69 = 69
	Nr70 = 70
	Nr71 = 71
	Nr72 = 72
	Nr73 = 73
	Nr74 = 74
	Nr75 = 75
	Nr76 = 76
	Nr77 = 77
	Nr78 = 78
	Nr79 = 79
	Nr80 = 80
	Nr81 = 81
	Nr82 = 82
	Nr83 = 83
	Nr84 = 84
	Nr85 = 85
	Nr86 = 86
	Nr87 = 87
	Nr88 = 88
	Nr89 = 89
	Nr90 = 90
	Nr91 = 91
	Nr92 = 92
	Nr93 = 93
	Nr94 = 94
	Nr95 = 95
	Nr96 = 96
	Nr97 = 97
	Nr98 = 98
	Nr99 = 99
	Nr100 = 100


# noinspection SpellCheckingInspection
class SetGroup(Enum):
	"""Repeated capability SetGroup"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2


# noinspection SpellCheckingInspection
class SetItem(Enum):
	"""Repeated capability SetItem"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2


# noinspection SpellCheckingInspection
class SfCfgIxNull(Enum):
	"""Repeated capability SfCfgIxNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31


# noinspection SpellCheckingInspection
class Slot(Enum):
	"""Repeated capability Slot"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16


# noinspection SpellCheckingInspection
class SlotNull(Enum):
	"""Repeated capability SlotNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15


# noinspection SpellCheckingInspection
class Station(Enum):
	"""Repeated capability Station"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16


# noinspection SpellCheckingInspection
class StepNull(Enum):
	"""Repeated capability StepNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32


# noinspection SpellCheckingInspection
class Stream(Enum):
	"""Repeated capability Stream"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16


# noinspection SpellCheckingInspection
class SubChannel(Enum):
	"""Repeated capability SubChannel"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16


# noinspection SpellCheckingInspection
class SubCluster(Enum):
	"""Repeated capability SubCluster"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3


# noinspection SpellCheckingInspection
class SubframeNull(Enum):
	"""Repeated capability SubframeNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63
	Nr64 = 64
	Nr65 = 65
	Nr66 = 66
	Nr67 = 67
	Nr68 = 68
	Nr69 = 69
	Nr70 = 70
	Nr71 = 71
	Nr72 = 72
	Nr73 = 73
	Nr74 = 74
	Nr75 = 75
	Nr76 = 76
	Nr77 = 77
	Nr78 = 78
	Nr79 = 79
	Nr80 = 80
	Nr81 = 81
	Nr82 = 82
	Nr83 = 83
	Nr84 = 84
	Nr85 = 85
	Nr86 = 86
	Nr87 = 87
	Nr88 = 88
	Nr89 = 89
	Nr90 = 90
	Nr91 = 91
	Nr92 = 92
	Nr93 = 93
	Nr94 = 94
	Nr95 = 95
	Nr96 = 96
	Nr97 = 97
	Nr98 = 98
	Nr99 = 99
	Nr100 = 100
	Nr101 = 101
	Nr102 = 102
	Nr103 = 103
	Nr104 = 104
	Nr105 = 105
	Nr106 = 106
	Nr107 = 107
	Nr108 = 108
	Nr109 = 109
	Nr110 = 110
	Nr111 = 111
	Nr112 = 112
	Nr113 = 113
	Nr114 = 114
	Nr115 = 115
	Nr116 = 116
	Nr117 = 117
	Nr118 = 118
	Nr119 = 119
	Nr120 = 120
	Nr121 = 121
	Nr122 = 122
	Nr123 = 123
	Nr124 = 124
	Nr125 = 125
	Nr126 = 126
	Nr127 = 127
	Nr128 = 128
	Nr129 = 129
	Nr130 = 130
	Nr131 = 131
	Nr132 = 132
	Nr133 = 133
	Nr134 = 134
	Nr135 = 135
	Nr136 = 136
	Nr137 = 137
	Nr138 = 138
	Nr139 = 139
	Nr140 = 140
	Nr141 = 141
	Nr142 = 142
	Nr143 = 143
	Nr144 = 144
	Nr145 = 145
	Nr146 = 146
	Nr147 = 147
	Nr148 = 148
	Nr149 = 149
	Nr150 = 150
	Nr151 = 151
	Nr152 = 152
	Nr153 = 153
	Nr154 = 154
	Nr155 = 155
	Nr156 = 156
	Nr157 = 157
	Nr158 = 158
	Nr159 = 159
	Nr160 = 160
	Nr161 = 161
	Nr162 = 162
	Nr163 = 163
	Nr164 = 164
	Nr165 = 165
	Nr166 = 166
	Nr167 = 167
	Nr168 = 168
	Nr169 = 169
	Nr170 = 170
	Nr171 = 171
	Nr172 = 172
	Nr173 = 173
	Nr174 = 174
	Nr175 = 175
	Nr176 = 176
	Nr177 = 177
	Nr178 = 178
	Nr179 = 179
	Nr180 = 180
	Nr181 = 181
	Nr182 = 182
	Nr183 = 183
	Nr184 = 184
	Nr185 = 185
	Nr186 = 186
	Nr187 = 187
	Nr188 = 188
	Nr189 = 189
	Nr190 = 190
	Nr191 = 191
	Nr192 = 192
	Nr193 = 193
	Nr194 = 194
	Nr195 = 195
	Nr196 = 196
	Nr197 = 197
	Nr198 = 198
	Nr199 = 199
	Nr200 = 200


# noinspection SpellCheckingInspection
class Subpacket(Enum):
	"""Repeated capability Subpacket"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16


# noinspection SpellCheckingInspection
class SubPath(Enum):
	"""Repeated capability SubPath"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20


# noinspection SpellCheckingInspection
class TciCodepoint(Enum):
	"""Repeated capability TciCodepoint"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8


# noinspection SpellCheckingInspection
class Terminal(Enum):
	"""Repeated capability Terminal"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4


# noinspection SpellCheckingInspection
class TestMode(Enum):
	"""Repeated capability TestMode"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4


# noinspection SpellCheckingInspection
class TimeSlot(Enum):
	"""Repeated capability TimeSlot"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8


# noinspection SpellCheckingInspection
class TmConnector(Enum):
	"""Repeated capability TmConnector"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3


# noinspection SpellCheckingInspection
class TransmGapLength(Enum):
	"""Repeated capability TransmGapLength"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16


# noinspection SpellCheckingInspection
class Transmission(Enum):
	"""Repeated capability Transmission"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32


# noinspection SpellCheckingInspection
class TransmissionChain(Enum):
	"""Repeated capability TransmissionChain"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8


# noinspection SpellCheckingInspection
class TransmTimeIntervalNull(Enum):
	"""Repeated capability TransmTimeIntervalNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63


# noinspection SpellCheckingInspection
class TransportChannelNull(Enum):
	"""Repeated capability TransportChannelNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48
	Nr49 = 49
	Nr50 = 50
	Nr51 = 51
	Nr52 = 52
	Nr53 = 53
	Nr54 = 54
	Nr55 = 55
	Nr56 = 56
	Nr57 = 57
	Nr58 = 58
	Nr59 = 59
	Nr60 = 60
	Nr61 = 61
	Nr62 = 62
	Nr63 = 63
	Nr64 = 64


# noinspection SpellCheckingInspection
class TriggerFrameUser(Enum):
	"""Repeated capability TriggerFrameUser"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37


# noinspection SpellCheckingInspection
class TwoStreams(Enum):
	"""Repeated capability TwoStreams"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2


# noinspection SpellCheckingInspection
class TypePy(Enum):
	"""Repeated capability TypePy"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3


# noinspection SpellCheckingInspection
class UlCarriersNull(Enum):
	"""Repeated capability UlCarriersNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4


# noinspection SpellCheckingInspection
class UserEquipment(Enum):
	"""Repeated capability UserEquipment"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16


# noinspection SpellCheckingInspection
class UserIx(Enum):
	"""Repeated capability UserIx"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47
	Nr48 = 48


# noinspection SpellCheckingInspection
class UserNull(Enum):
	"""Repeated capability UserNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
	Nr32 = 32
	Nr33 = 33
	Nr34 = 34
	Nr35 = 35
	Nr36 = 36
	Nr37 = 37
	Nr38 = 38
	Nr39 = 39
	Nr40 = 40
	Nr41 = 41
	Nr42 = 42
	Nr43 = 43
	Nr44 = 44
	Nr45 = 45
	Nr46 = 46
	Nr47 = 47


# noinspection SpellCheckingInspection
class VdbTransmitter(Enum):
	"""Repeated capability VdbTransmitter"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8


# noinspection SpellCheckingInspection
class Vehicle(Enum):
	"""Repeated capability Vehicle"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr1 = 1
	Nr2 = 2


# noinspection SpellCheckingInspection
class ZoneNull(Enum):
	"""Repeated capability ZoneNull"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Nr0 = 0
	Nr1 = 1
	Nr2 = 2
	Nr3 = 3
	Nr4 = 4
	Nr5 = 5
	Nr6 = 6
	Nr7 = 7
	Nr8 = 8
	Nr9 = 9
	Nr10 = 10
	Nr11 = 11
	Nr12 = 12
	Nr13 = 13
	Nr14 = 14
	Nr15 = 15
	Nr16 = 16
	Nr17 = 17
	Nr18 = 18
	Nr19 = 19
	Nr20 = 20
	Nr21 = 21
	Nr22 = 22
	Nr23 = 23
	Nr24 = 24
	Nr25 = 25
	Nr26 = 26
	Nr27 = 27
	Nr28 = 28
	Nr29 = 29
	Nr30 = 30
	Nr31 = 31
