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
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack111111l1l1_opy_ import (
    bstack1llllllllll_opy_,
    bstack1111l11lll_opy_,
    bstack111111l11l_opy_,
    bstack1111l11l11_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1llll1111ll_opy_(bstack1llllllllll_opy_):
    bstack1l1l11111l1_opy_ = bstack1l11l1l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢፇ")
    bstack1l1ll111l11_opy_ = bstack1l11l1l_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣፈ")
    bstack1l1ll111l1l_opy_ = bstack1l11l1l_opy_ (u"ࠤ࡫ࡹࡧࡥࡵࡳ࡮ࠥፉ")
    bstack1l1ll11lll1_opy_ = bstack1l11l1l_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤፊ")
    bstack1l1l1111l1l_opy_ = bstack1l11l1l_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࠢፋ")
    bstack1l1l111111l_opy_ = bstack1l11l1l_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࡢࡵࡼࡲࡨࠨፌ")
    NAME = bstack1l11l1l_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥፍ")
    bstack1l11lllll11_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1l11l11_opy_: Any
    bstack1l11lllll1l_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1l11l1l_opy_ (u"ࠢ࡭ࡣࡸࡲࡨ࡮ࠢፎ"), bstack1l11l1l_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࠤፏ"), bstack1l11l1l_opy_ (u"ࠤࡱࡩࡼࡥࡰࡢࡩࡨࠦፐ"), bstack1l11l1l_opy_ (u"ࠥࡧࡱࡵࡳࡦࠤፑ"), bstack1l11l1l_opy_ (u"ࠦࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠨፒ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1llllllll11_opy_(methods)
    def bstack11111ll11l_opy_(self, instance: bstack1111l11lll_opy_, method_name: str, bstack1111l1l11l_opy_: timedelta, *args, **kwargs):
        pass
    def bstack111111llll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1111l11lll_opy_, str],
        bstack1llllllll1l_opy_: Tuple[bstack111111l11l_opy_, bstack1111l11l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1lllllllll1_opy_, bstack1l11lllllll_opy_ = bstack1llllllll1l_opy_
        bstack1l11llllll1_opy_ = bstack1llll1111ll_opy_.bstack1l1l11111ll_opy_(bstack1llllllll1l_opy_)
        if bstack1l11llllll1_opy_ in bstack1llll1111ll_opy_.bstack1l11lllll11_opy_:
            bstack1l1l1111l11_opy_ = None
            for callback in bstack1llll1111ll_opy_.bstack1l11lllll11_opy_[bstack1l11llllll1_opy_]:
                try:
                    bstack1l1l1111111_opy_ = callback(self, target, exec, bstack1llllllll1l_opy_, result, *args, **kwargs)
                    if bstack1l1l1111l11_opy_ == None:
                        bstack1l1l1111l11_opy_ = bstack1l1l1111111_opy_
                except Exception as e:
                    self.logger.error(bstack1l11l1l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࠥፓ") + str(e) + bstack1l11l1l_opy_ (u"ࠨࠢፔ"))
                    traceback.print_exc()
            if bstack1l11lllllll_opy_ == bstack1111l11l11_opy_.PRE and callable(bstack1l1l1111l11_opy_):
                return bstack1l1l1111l11_opy_
            elif bstack1l11lllllll_opy_ == bstack1111l11l11_opy_.POST and bstack1l1l1111l11_opy_:
                return bstack1l1l1111l11_opy_
    def bstack11111l1ll1_opy_(
        self, method_name, previous_state: bstack111111l11l_opy_, *args, **kwargs
    ) -> bstack111111l11l_opy_:
        if method_name == bstack1l11l1l_opy_ (u"ࠧ࡭ࡣࡸࡲࡨ࡮ࠧፕ") or method_name == bstack1l11l1l_opy_ (u"ࠨࡥࡲࡲࡳ࡫ࡣࡵࠩፖ") or method_name == bstack1l11l1l_opy_ (u"ࠩࡱࡩࡼࡥࡰࡢࡩࡨࠫፗ"):
            return bstack111111l11l_opy_.bstack1111l1l111_opy_
        if method_name == bstack1l11l1l_opy_ (u"ࠪࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠬፘ"):
            return bstack111111l11l_opy_.bstack11111111ll_opy_
        if method_name == bstack1l11l1l_opy_ (u"ࠫࡨࡲ࡯ࡴࡧࠪፙ"):
            return bstack111111l11l_opy_.QUIT
        return bstack111111l11l_opy_.NONE
    @staticmethod
    def bstack1l1l11111ll_opy_(bstack1llllllll1l_opy_: Tuple[bstack111111l11l_opy_, bstack1111l11l11_opy_]):
        return bstack1l11l1l_opy_ (u"ࠧࡀࠢፚ").join((bstack111111l11l_opy_(bstack1llllllll1l_opy_[0]).name, bstack1111l11l11_opy_(bstack1llllllll1l_opy_[1]).name))
    @staticmethod
    def bstack1ll1lll111l_opy_(bstack1llllllll1l_opy_: Tuple[bstack111111l11l_opy_, bstack1111l11l11_opy_], callback: Callable):
        bstack1l11llllll1_opy_ = bstack1llll1111ll_opy_.bstack1l1l11111ll_opy_(bstack1llllllll1l_opy_)
        if not bstack1l11llllll1_opy_ in bstack1llll1111ll_opy_.bstack1l11lllll11_opy_:
            bstack1llll1111ll_opy_.bstack1l11lllll11_opy_[bstack1l11llllll1_opy_] = []
        bstack1llll1111ll_opy_.bstack1l11lllll11_opy_[bstack1l11llllll1_opy_].append(callback)
    @staticmethod
    def bstack1ll1ll1l1l1_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll1l111l11_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll1l111l1l_opy_(instance: bstack1111l11lll_opy_, default_value=None):
        return bstack1llllllllll_opy_.bstack1111l11111_opy_(instance, bstack1llll1111ll_opy_.bstack1l1ll11lll1_opy_, default_value)
    @staticmethod
    def bstack1ll1l1l1ll1_opy_(instance: bstack1111l11lll_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll11llllll_opy_(instance: bstack1111l11lll_opy_, default_value=None):
        return bstack1llllllllll_opy_.bstack1111l11111_opy_(instance, bstack1llll1111ll_opy_.bstack1l1ll111l1l_opy_, default_value)
    @staticmethod
    def bstack1ll11llll1l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1l1l1l1l_opy_(method_name: str, *args):
        if not bstack1llll1111ll_opy_.bstack1ll1ll1l1l1_opy_(method_name):
            return False
        if not bstack1llll1111ll_opy_.bstack1l1l1111l1l_opy_ in bstack1llll1111ll_opy_.bstack1l1l11l111l_opy_(*args):
            return False
        bstack1ll11ll1lll_opy_ = bstack1llll1111ll_opy_.bstack1ll11ll1l1l_opy_(*args)
        return bstack1ll11ll1lll_opy_ and bstack1l11l1l_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨ፛") in bstack1ll11ll1lll_opy_ and bstack1l11l1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣ፜") in bstack1ll11ll1lll_opy_[bstack1l11l1l_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣ፝")]
    @staticmethod
    def bstack1ll1ll11ll1_opy_(method_name: str, *args):
        if not bstack1llll1111ll_opy_.bstack1ll1ll1l1l1_opy_(method_name):
            return False
        if not bstack1llll1111ll_opy_.bstack1l1l1111l1l_opy_ in bstack1llll1111ll_opy_.bstack1l1l11l111l_opy_(*args):
            return False
        bstack1ll11ll1lll_opy_ = bstack1llll1111ll_opy_.bstack1ll11ll1l1l_opy_(*args)
        return (
            bstack1ll11ll1lll_opy_
            and bstack1l11l1l_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤ፞") in bstack1ll11ll1lll_opy_
            and bstack1l11l1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡤࡴ࡬ࡴࡹࠨ፟") in bstack1ll11ll1lll_opy_[bstack1l11l1l_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦ፠")]
        )
    @staticmethod
    def bstack1l1l11l111l_opy_(*args):
        return str(bstack1llll1111ll_opy_.bstack1ll11llll1l_opy_(*args)).lower()