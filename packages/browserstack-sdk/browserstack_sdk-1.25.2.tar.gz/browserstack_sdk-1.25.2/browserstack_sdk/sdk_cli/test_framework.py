# coding: UTF-8
import sys
bstack111ll_opy_ = sys.version_info [0] == 2
bstack11l11l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11l1l_opy_ (bstack111_opy_):
    global bstack1111l1_opy_
    bstack1l1ll1_opy_ = ord (bstack111_opy_ [-1])
    bstack1l1l_opy_ = bstack111_opy_ [:-1]
    bstack11l1111_opy_ = bstack1l1ll1_opy_ % len (bstack1l1l_opy_)
    bstack1l1_opy_ = bstack1l1l_opy_ [:bstack11l1111_opy_] + bstack1l1l_opy_ [bstack11l1111_opy_:]
    if bstack111ll_opy_:
        bstack111lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l1_opy_ - (bstack11lllll_opy_ + bstack1l1ll1_opy_) % bstack1l11l11_opy_) for bstack11lllll_opy_, char in enumerate (bstack1l1_opy_)])
    else:
        bstack111lll_opy_ = str () .join ([chr (ord (char) - bstack11l11l1_opy_ - (bstack11lllll_opy_ + bstack1l1ll1_opy_) % bstack1l11l11_opy_) for bstack11lllll_opy_, char in enumerate (bstack1l1_opy_)])
    return eval (bstack111lll_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1111l1llll_opy_ import bstack1111l1lll1_opy_
from browserstack_sdk.sdk_cli.bstack111111111l_opy_ import bstack11111l111l_opy_, bstack11111ll1l1_opy_
class bstack1lll11111ll_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l11l1l_opy_ (u"࡙ࠦ࡫ࡳࡵࡊࡲࡳࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢᓨ").format(self.name)
class bstack1lllll11l11_opy_(Enum):
    NONE = 0
    BEFORE_ALL = 1
    LOG = 2
    SETUP_FIXTURE = 3
    INIT_TEST = 4
    BEFORE_EACH = 5
    AFTER_EACH = 6
    TEST = 7
    STEP = 8
    LOG_REPORT = 9
    AFTER_ALL = 10
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack1l11l1l_opy_ (u"࡚ࠧࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨᓩ").format(self.name)
class bstack1lll1l11l1l_opy_(bstack11111l111l_opy_):
    bstack1ll1ll111l1_opy_: List[str]
    bstack1l111llll11_opy_: Dict[str, str]
    state: bstack1lllll11l11_opy_
    bstack1111111l11_opy_: datetime
    bstack11111l1l11_opy_: datetime
    def __init__(
        self,
        context: bstack11111ll1l1_opy_,
        bstack1ll1ll111l1_opy_: List[str],
        bstack1l111llll11_opy_: Dict[str, str],
        state=bstack1lllll11l11_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll1ll111l1_opy_ = bstack1ll1ll111l1_opy_
        self.bstack1l111llll11_opy_ = bstack1l111llll11_opy_
        self.state = state
        self.bstack1111111l11_opy_ = datetime.now(tz=timezone.utc)
        self.bstack11111l1l11_opy_ = datetime.now(tz=timezone.utc)
    def bstack11111l1111_opy_(self, bstack111111ll1l_opy_: bstack1lllll11l11_opy_):
        bstack111111ll11_opy_ = bstack1lllll11l11_opy_(bstack111111ll1l_opy_).name
        if not bstack111111ll11_opy_:
            return False
        if bstack111111ll1l_opy_ == self.state:
            return False
        self.state = bstack111111ll1l_opy_
        self.bstack11111l1l11_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l11l111l1l_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1lll1l1ll1l_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1lll11ll1_opy_: int = None
    bstack1l1llll1ll1_opy_: str = None
    bstack1ll1l11_opy_: str = None
    bstack111lll1ll_opy_: str = None
    bstack1ll111111l1_opy_: str = None
    bstack1l11lll1l1l_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll1l1111l1_opy_ = bstack1l11l1l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡺࡻࡩࡥࠤᓪ")
    bstack1l11l1lllll_opy_ = bstack1l11l1l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡯ࡤࠣᓫ")
    bstack1ll1l11ll11_opy_ = bstack1l11l1l_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠦᓬ")
    bstack1l11lll1lll_opy_ = bstack1l11l1l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡤࡶࡡࡵࡪࠥᓭ")
    bstack1l11l11l1l1_opy_ = bstack1l11l1l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡶࡤ࡫ࡸࠨᓮ")
    bstack1l1l1ll1l11_opy_ = bstack1l11l1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᓯ")
    bstack1ll1111l111_opy_ = bstack1l11l1l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡹࡵ࡭ࡶࡢࡥࡹࠨᓰ")
    bstack1ll11l1111l_opy_ = bstack1l11l1l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᓱ")
    bstack1l1llll11l1_opy_ = bstack1l11l1l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡫࡮ࡥࡧࡧࡣࡦࡺࠢᓲ")
    bstack1l11ll111ll_opy_ = bstack1l11l1l_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᓳ")
    bstack1ll1l1ll11l_opy_ = bstack1l11l1l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠣᓴ")
    bstack1ll11l111l1_opy_ = bstack1l11l1l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧᓵ")
    bstack1l111lll111_opy_ = bstack1l11l1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡦࡳࡩ࡫ࠢᓶ")
    bstack1l1ll1l1l11_opy_ = bstack1l11l1l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠢᓷ")
    bstack1ll1l11l111_opy_ = bstack1l11l1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠢᓸ")
    bstack1l1l1llll11_opy_ = bstack1l11l1l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡡࡪ࡮ࡸࡶࡪࠨᓹ")
    bstack1l11l11l1ll_opy_ = bstack1l11l1l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠧᓺ")
    bstack1l11ll1lll1_opy_ = bstack1l11l1l_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡭ࡱࡪࡷࠧᓻ")
    bstack1l11ll1l1ll_opy_ = bstack1l11l1l_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡯ࡨࡸࡦࠨᓼ")
    bstack1l111l1l11l_opy_ = bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡶࡧࡴࡶࡥࡴࠩᓽ")
    bstack1l1l1111lll_opy_ = bstack1l11l1l_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨᓾ")
    bstack1l11l1l11ll_opy_ = bstack1l11l1l_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᓿ")
    bstack1l11ll1111l_opy_ = bstack1l11l1l_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡥ࡯ࡦࡨࡨࡤࡧࡴࠣᔀ")
    bstack1l11ll11lll_opy_ = bstack1l11l1l_opy_ (u"ࠣࡪࡲࡳࡰࡥࡩࡥࠤᔁ")
    bstack1l11lll111l_opy_ = bstack1l11l1l_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡳࡧࡶࡹࡱࡺࠢᔂ")
    bstack1l111ll1lll_opy_ = bstack1l11l1l_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠ࡮ࡲ࡫ࡸࠨᔃ")
    bstack1l11l1111ll_opy_ = bstack1l11l1l_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠢᔄ")
    bstack1l111lll1l1_opy_ = bstack1l11l1l_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᔅ")
    bstack1l11l11ll1l_opy_ = bstack1l11l1l_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣᔆ")
    bstack1l11l1llll1_opy_ = bstack1l11l1l_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣᔇ")
    bstack1l11llll11l_opy_ = bstack1l11l1l_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤᔈ")
    bstack1ll11111111_opy_ = bstack1l11l1l_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠦᔉ")
    bstack1ll1111ll1l_opy_ = bstack1l11l1l_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡎࡒࡋࠧᔊ")
    bstack1l1ll1lllll_opy_ = bstack1l11l1l_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᔋ")
    bstack11111l11l1_opy_: Dict[str, bstack1lll1l11l1l_opy_] = dict()
    bstack1l111l11111_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll1ll111l1_opy_: List[str]
    bstack1l111llll11_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll1ll111l1_opy_: List[str],
        bstack1l111llll11_opy_: Dict[str, str],
        bstack1111l1llll_opy_: bstack1111l1lll1_opy_
    ):
        self.bstack1ll1ll111l1_opy_ = bstack1ll1ll111l1_opy_
        self.bstack1l111llll11_opy_ = bstack1l111llll11_opy_
        self.bstack1111l1llll_opy_ = bstack1111l1llll_opy_
    def track_event(
        self,
        context: bstack1l11l111l1l_opy_,
        test_framework_state: bstack1lllll11l11_opy_,
        test_hook_state: bstack1lll11111ll_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1l11l1l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥࡧࡲࡨࡵࡀࡿࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻࡾࠤᔌ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l11lll11l1_opy_(
        self,
        instance: bstack1lll1l11l1l_opy_,
        bstack1llllllll1l_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll11111ll_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11llllll1_opy_ = TestFramework.bstack1l1l11111ll_opy_(bstack1llllllll1l_opy_)
        if not bstack1l11llllll1_opy_ in TestFramework.bstack1l111l11111_opy_:
            return
        self.logger.debug(bstack1l11l1l_opy_ (u"ࠨࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡽࢀࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡹࠢᔍ").format(len(TestFramework.bstack1l111l11111_opy_[bstack1l11llllll1_opy_])))
        for callback in TestFramework.bstack1l111l11111_opy_[bstack1l11llllll1_opy_]:
            try:
                callback(self, instance, bstack1llllllll1l_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1l11l1l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠢᔎ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1lll1ll11_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1lll11l11_opy_(self, instance, bstack1llllllll1l_opy_):
        return
    @abc.abstractmethod
    def bstack1ll111ll1ll_opy_(self, instance, bstack1llllllll1l_opy_):
        return
    @staticmethod
    def bstack1111111ll1_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack11111l111l_opy_.create_context(target)
        instance = TestFramework.bstack11111l11l1_opy_.get(ctx.id, None)
        if instance and instance.bstack11111llll1_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1lll1111l_opy_(reverse=True) -> List[bstack1lll1l11l1l_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack11111l11l1_opy_.values(),
            ),
            key=lambda t: t.bstack1111111l11_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111ll1ll_opy_(ctx: bstack11111ll1l1_opy_, reverse=True) -> List[bstack1lll1l11l1l_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack11111l11l1_opy_.values(),
            ),
            key=lambda t: t.bstack1111111l11_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1111111lll_opy_(instance: bstack1lll1l11l1l_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1111l11111_opy_(instance: bstack1lll1l11l1l_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack11111l1111_opy_(instance: bstack1lll1l11l1l_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l11l1l_opy_ (u"ࠣࡵࡨࡸࡤࡹࡴࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣ࡯ࡪࡿ࠽ࡼࡿࠣࡺࡦࡲࡵࡦ࠿ࡾࢁࠧᔏ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11ll11l11_opy_(instance: bstack1lll1l11l1l_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1l11l1l_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥ࡫࡮ࡵࡴ࡬ࡩࡸࡃࡻࡾࠤᔐ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack1l1111ll11l_opy_(instance: bstack1lllll11l11_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l11l1l_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡭ࡨࡽࡂࢁࡽࠡࡸࡤࡰࡺ࡫࠽ࡼࡿࠥᔑ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1111111ll1_opy_(target, strict)
        return TestFramework.bstack1111l11111_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1111111ll1_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11ll11111_opy_(instance: bstack1lll1l11l1l_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l11ll1l111_opy_(instance: bstack1lll1l11l1l_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l1l11111ll_opy_(bstack1llllllll1l_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll11111ll_opy_]):
        return bstack1l11l1l_opy_ (u"ࠦ࠿ࠨᔒ").join((bstack1lllll11l11_opy_(bstack1llllllll1l_opy_[0]).name, bstack1lll11111ll_opy_(bstack1llllllll1l_opy_[1]).name))
    @staticmethod
    def bstack1ll1lll111l_opy_(bstack1llllllll1l_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll11111ll_opy_], callback: Callable):
        bstack1l11llllll1_opy_ = TestFramework.bstack1l1l11111ll_opy_(bstack1llllllll1l_opy_)
        TestFramework.logger.debug(bstack1l11l1l_opy_ (u"ࠧࡹࡥࡵࡡ࡫ࡳࡴࡱ࡟ࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣ࡬ࡴࡵ࡫ࡠࡴࡨ࡫࡮ࡹࡴࡳࡻࡢ࡯ࡪࡿ࠽ࡼࡿࠥᔓ").format(bstack1l11llllll1_opy_))
        if not bstack1l11llllll1_opy_ in TestFramework.bstack1l111l11111_opy_:
            TestFramework.bstack1l111l11111_opy_[bstack1l11llllll1_opy_] = []
        TestFramework.bstack1l111l11111_opy_[bstack1l11llllll1_opy_].append(callback)
    @staticmethod
    def bstack1l1lll1lll1_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1l11l1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡸ࡮ࡴࡳࠣᔔ"):
            return klass.__qualname__
        return module + bstack1l11l1l_opy_ (u"ࠢ࠯ࠤᔕ") + klass.__qualname__
    @staticmethod
    def bstack1l1lll1l111_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}