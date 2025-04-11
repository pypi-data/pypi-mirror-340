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
from bstack_utils.bstack1111l11l_opy_ import bstack1lllll11l1l_opy_
from bstack_utils.constants import EVENTS
class bstack1llll11lll1_opy_(bstack1llllllllll_opy_):
    bstack1l1l11111l1_opy_ = bstack1l11l1l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥᒯ")
    NAME = bstack1l11l1l_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨᒰ")
    bstack1l1ll111l1l_opy_ = bstack1l11l1l_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࠨᒱ")
    bstack1l1ll111l11_opy_ = bstack1l11l1l_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᒲ")
    bstack1l111l111l1_opy_ = bstack1l11l1l_opy_ (u"ࠢࡪࡰࡳࡹࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧᒳ")
    bstack1l1ll11lll1_opy_ = bstack1l11l1l_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᒴ")
    bstack1l1l111l1ll_opy_ = bstack1l11l1l_opy_ (u"ࠤ࡬ࡷࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡭ࡻࡢࠣᒵ")
    bstack1l111l1111l_opy_ = bstack1l11l1l_opy_ (u"ࠥࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᒶ")
    bstack1l1111llll1_opy_ = bstack1l11l1l_opy_ (u"ࠦࡪࡴࡤࡦࡦࡢࡥࡹࠨᒷ")
    bstack1ll1l11l111_opy_ = bstack1l11l1l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࠨᒸ")
    bstack1l1l1l11lll_opy_ = bstack1l11l1l_opy_ (u"ࠨ࡮ࡦࡹࡶࡩࡸࡹࡩࡰࡰࠥᒹ")
    bstack1l1111lllll_opy_ = bstack1l11l1l_opy_ (u"ࠢࡨࡧࡷࠦᒺ")
    bstack1ll111l1ll1_opy_ = bstack1l11l1l_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᒻ")
    bstack1l1l1111l1l_opy_ = bstack1l11l1l_opy_ (u"ࠤࡺ࠷ࡨ࡫ࡸࡦࡥࡸࡸࡪࡹࡣࡳ࡫ࡳࡸࠧᒼ")
    bstack1l1l111111l_opy_ = bstack1l11l1l_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࡧࡳࡺࡰࡦࠦᒽ")
    bstack1l1111ll1l1_opy_ = bstack1l11l1l_opy_ (u"ࠦࡶࡻࡩࡵࠤᒾ")
    bstack1l111l11111_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l11l1lll_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1lll1l11l11_opy_: Any
    bstack1l11lllll1l_opy_: Dict
    def __init__(
        self,
        bstack1l1l11l1lll_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1lll1l11l11_opy_: Dict[str, Any],
        methods=[bstack1l11l1l_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢᒿ"), bstack1l11l1l_opy_ (u"ࠨࡳࡵࡣࡵࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࠨᓀ"), bstack1l11l1l_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᓁ"), bstack1l11l1l_opy_ (u"ࠣࡳࡸ࡭ࡹࠨᓂ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l1l11l1lll_opy_ = bstack1l1l11l1lll_opy_
        self.platform_index = platform_index
        self.bstack1llllllll11_opy_(methods)
        self.bstack1lll1l11l11_opy_ = bstack1lll1l11l11_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1llllllllll_opy_.get_data(bstack1llll11lll1_opy_.bstack1l1ll111l11_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1llllllllll_opy_.get_data(bstack1llll11lll1_opy_.bstack1l1ll111l1l_opy_, target, strict)
    @staticmethod
    def bstack1l1111lll11_opy_(target: object, strict=True):
        return bstack1llllllllll_opy_.get_data(bstack1llll11lll1_opy_.bstack1l111l111l1_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1llllllllll_opy_.get_data(bstack1llll11lll1_opy_.bstack1l1ll11lll1_opy_, target, strict)
    @staticmethod
    def bstack1ll1l1l1ll1_opy_(instance: bstack1111l11lll_opy_) -> bool:
        return bstack1llllllllll_opy_.bstack1111l11111_opy_(instance, bstack1llll11lll1_opy_.bstack1l1l111l1ll_opy_, False)
    @staticmethod
    def bstack1ll11llllll_opy_(instance: bstack1111l11lll_opy_, default_value=None):
        return bstack1llllllllll_opy_.bstack1111l11111_opy_(instance, bstack1llll11lll1_opy_.bstack1l1ll111l1l_opy_, default_value)
    @staticmethod
    def bstack1ll1l111l1l_opy_(instance: bstack1111l11lll_opy_, default_value=None):
        return bstack1llllllllll_opy_.bstack1111l11111_opy_(instance, bstack1llll11lll1_opy_.bstack1l1ll11lll1_opy_, default_value)
    @staticmethod
    def bstack1ll11ll1l11_opy_(hub_url: str, bstack1l1111lll1l_opy_=bstack1l11l1l_opy_ (u"ࠤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࠨᓃ")):
        try:
            bstack1l1111ll1ll_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack1l1111ll1ll_opy_.endswith(bstack1l1111lll1l_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll1ll1l1l1_opy_(method_name: str):
        return method_name == bstack1l11l1l_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᓄ")
    @staticmethod
    def bstack1ll1l111l11_opy_(method_name: str, *args):
        return (
            bstack1llll11lll1_opy_.bstack1ll1ll1l1l1_opy_(method_name)
            and bstack1llll11lll1_opy_.bstack1l1l11l111l_opy_(*args) == bstack1llll11lll1_opy_.bstack1l1l1l11lll_opy_
        )
    @staticmethod
    def bstack1ll1l1l1l1l_opy_(method_name: str, *args):
        if not bstack1llll11lll1_opy_.bstack1ll1ll1l1l1_opy_(method_name):
            return False
        if not bstack1llll11lll1_opy_.bstack1l1l1111l1l_opy_ in bstack1llll11lll1_opy_.bstack1l1l11l111l_opy_(*args):
            return False
        bstack1ll11ll1lll_opy_ = bstack1llll11lll1_opy_.bstack1ll11ll1l1l_opy_(*args)
        return bstack1ll11ll1lll_opy_ and bstack1l11l1l_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᓅ") in bstack1ll11ll1lll_opy_ and bstack1l11l1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᓆ") in bstack1ll11ll1lll_opy_[bstack1l11l1l_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᓇ")]
    @staticmethod
    def bstack1ll1ll11ll1_opy_(method_name: str, *args):
        if not bstack1llll11lll1_opy_.bstack1ll1ll1l1l1_opy_(method_name):
            return False
        if not bstack1llll11lll1_opy_.bstack1l1l1111l1l_opy_ in bstack1llll11lll1_opy_.bstack1l1l11l111l_opy_(*args):
            return False
        bstack1ll11ll1lll_opy_ = bstack1llll11lll1_opy_.bstack1ll11ll1l1l_opy_(*args)
        return (
            bstack1ll11ll1lll_opy_
            and bstack1l11l1l_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢᓈ") in bstack1ll11ll1lll_opy_
            and bstack1l11l1l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸࡩࡲࡪࡲࡷࠦᓉ") in bstack1ll11ll1lll_opy_[bstack1l11l1l_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᓊ")]
        )
    @staticmethod
    def bstack1l1l11l111l_opy_(*args):
        return str(bstack1llll11lll1_opy_.bstack1ll11llll1l_opy_(*args)).lower()
    @staticmethod
    def bstack1ll11llll1l_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11ll1l1l_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack11l1l1l1l_opy_(driver):
        command_executor = getattr(driver, bstack1l11l1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᓋ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1l11l1l_opy_ (u"ࠦࡤࡻࡲ࡭ࠤᓌ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1l11l1l_opy_ (u"ࠧࡥࡣ࡭࡫ࡨࡲࡹࡥࡣࡰࡰࡩ࡭࡬ࠨᓍ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1l11l1l_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪࡥࡳࡦࡴࡹࡩࡷࡥࡡࡥࡦࡵࠦᓎ"), None)
        return hub_url
    def bstack1l1l1l11111_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1l11l1l_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᓏ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1l11l1l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᓐ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1l11l1l_opy_ (u"ࠤࡢࡹࡷࡲࠢᓑ")):
                setattr(command_executor, bstack1l11l1l_opy_ (u"ࠥࡣࡺࡸ࡬ࠣᓒ"), hub_url)
                result = True
        if result:
            self.bstack1l1l11l1lll_opy_ = hub_url
            bstack1llll11lll1_opy_.bstack11111l1111_opy_(instance, bstack1llll11lll1_opy_.bstack1l1ll111l1l_opy_, hub_url)
            bstack1llll11lll1_opy_.bstack11111l1111_opy_(
                instance, bstack1llll11lll1_opy_.bstack1l1l111l1ll_opy_, bstack1llll11lll1_opy_.bstack1ll11ll1l11_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l1l11111ll_opy_(bstack1llllllll1l_opy_: Tuple[bstack111111l11l_opy_, bstack1111l11l11_opy_]):
        return bstack1l11l1l_opy_ (u"ࠦ࠿ࠨᓓ").join((bstack111111l11l_opy_(bstack1llllllll1l_opy_[0]).name, bstack1111l11l11_opy_(bstack1llllllll1l_opy_[1]).name))
    @staticmethod
    def bstack1ll1lll111l_opy_(bstack1llllllll1l_opy_: Tuple[bstack111111l11l_opy_, bstack1111l11l11_opy_], callback: Callable):
        bstack1l11llllll1_opy_ = bstack1llll11lll1_opy_.bstack1l1l11111ll_opy_(bstack1llllllll1l_opy_)
        if not bstack1l11llllll1_opy_ in bstack1llll11lll1_opy_.bstack1l111l11111_opy_:
            bstack1llll11lll1_opy_.bstack1l111l11111_opy_[bstack1l11llllll1_opy_] = []
        bstack1llll11lll1_opy_.bstack1l111l11111_opy_[bstack1l11llllll1_opy_].append(callback)
    def bstack11111ll11l_opy_(self, instance: bstack1111l11lll_opy_, method_name: str, bstack1111l1l11l_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1l11l1l_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᓔ")):
            return
        cmd = args[0] if method_name == bstack1l11l1l_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࠢᓕ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack1l111l111ll_opy_ = bstack1l11l1l_opy_ (u"ࠢ࠻ࠤᓖ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1ll111l11_opy_(bstack1l11l1l_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠤᓗ") + bstack1l111l111ll_opy_, bstack1111l1l11l_opy_)
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
        bstack1l11llllll1_opy_ = bstack1llll11lll1_opy_.bstack1l1l11111ll_opy_(bstack1llllllll1l_opy_)
        self.logger.debug(bstack1l11l1l_opy_ (u"ࠤࡲࡲࡤ࡮࡯ࡰ࡭࠽ࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᓘ") + str(kwargs) + bstack1l11l1l_opy_ (u"ࠥࠦᓙ"))
        if bstack1lllllllll1_opy_ == bstack111111l11l_opy_.QUIT:
            if bstack1l11lllllll_opy_ == bstack1111l11l11_opy_.PRE:
                bstack1ll1ll1ll1l_opy_ = bstack1lllll11l1l_opy_.bstack1ll11llll11_opy_(EVENTS.bstack11ll11l11l_opy_.value)
                bstack1llllllllll_opy_.bstack11111l1111_opy_(instance, EVENTS.bstack11ll11l11l_opy_.value, bstack1ll1ll1ll1l_opy_)
                self.logger.debug(bstack1l11l1l_opy_ (u"ࠦ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠣᓚ").format(instance, method_name, bstack1lllllllll1_opy_, bstack1l11lllllll_opy_))
        if bstack1lllllllll1_opy_ == bstack111111l11l_opy_.bstack1111l1l111_opy_:
            if bstack1l11lllllll_opy_ == bstack1111l11l11_opy_.POST and not bstack1llll11lll1_opy_.bstack1l1ll111l11_opy_ in instance.data:
                session_id = getattr(target, bstack1l11l1l_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᓛ"), None)
                if session_id:
                    instance.data[bstack1llll11lll1_opy_.bstack1l1ll111l11_opy_] = session_id
        elif (
            bstack1lllllllll1_opy_ == bstack111111l11l_opy_.bstack111111lll1_opy_
            and bstack1llll11lll1_opy_.bstack1l1l11l111l_opy_(*args) == bstack1llll11lll1_opy_.bstack1l1l1l11lll_opy_
        ):
            if bstack1l11lllllll_opy_ == bstack1111l11l11_opy_.PRE:
                hub_url = bstack1llll11lll1_opy_.bstack11l1l1l1l_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1llll11lll1_opy_.bstack1l1ll111l1l_opy_: hub_url,
                            bstack1llll11lll1_opy_.bstack1l1l111l1ll_opy_: bstack1llll11lll1_opy_.bstack1ll11ll1l11_opy_(hub_url),
                            bstack1llll11lll1_opy_.bstack1ll1l11l111_opy_: int(
                                os.environ.get(bstack1l11l1l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨᓜ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll11ll1lll_opy_ = bstack1llll11lll1_opy_.bstack1ll11ll1l1l_opy_(*args)
                bstack1l1111lll11_opy_ = bstack1ll11ll1lll_opy_.get(bstack1l11l1l_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᓝ"), None) if bstack1ll11ll1lll_opy_ else None
                if isinstance(bstack1l1111lll11_opy_, dict):
                    instance.data[bstack1llll11lll1_opy_.bstack1l111l111l1_opy_] = copy.deepcopy(bstack1l1111lll11_opy_)
                    instance.data[bstack1llll11lll1_opy_.bstack1l1ll11lll1_opy_] = bstack1l1111lll11_opy_
            elif bstack1l11lllllll_opy_ == bstack1111l11l11_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1l11l1l_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᓞ"), dict()).get(bstack1l11l1l_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡌࡨࠧᓟ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1llll11lll1_opy_.bstack1l1ll111l11_opy_: framework_session_id,
                                bstack1llll11lll1_opy_.bstack1l111l1111l_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1lllllllll1_opy_ == bstack111111l11l_opy_.bstack111111lll1_opy_
            and bstack1llll11lll1_opy_.bstack1l1l11l111l_opy_(*args) == bstack1llll11lll1_opy_.bstack1l1111ll1l1_opy_
            and bstack1l11lllllll_opy_ == bstack1111l11l11_opy_.POST
        ):
            instance.data[bstack1llll11lll1_opy_.bstack1l1111llll1_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l11llllll1_opy_ in bstack1llll11lll1_opy_.bstack1l111l11111_opy_:
            bstack1l1l1111l11_opy_ = None
            for callback in bstack1llll11lll1_opy_.bstack1l111l11111_opy_[bstack1l11llllll1_opy_]:
                try:
                    bstack1l1l1111111_opy_ = callback(self, target, exec, bstack1llllllll1l_opy_, result, *args, **kwargs)
                    if bstack1l1l1111l11_opy_ == None:
                        bstack1l1l1111l11_opy_ = bstack1l1l1111111_opy_
                except Exception as e:
                    self.logger.error(bstack1l11l1l_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࠣᓠ") + str(e) + bstack1l11l1l_opy_ (u"ࠦࠧᓡ"))
                    traceback.print_exc()
            if bstack1lllllllll1_opy_ == bstack111111l11l_opy_.QUIT:
                if bstack1l11lllllll_opy_ == bstack1111l11l11_opy_.POST:
                    bstack1ll1ll1ll1l_opy_ = bstack1llllllllll_opy_.bstack1111l11111_opy_(instance, EVENTS.bstack11ll11l11l_opy_.value)
                    if bstack1ll1ll1ll1l_opy_!=None:
                        bstack1lllll11l1l_opy_.end(EVENTS.bstack11ll11l11l_opy_.value, bstack1ll1ll1ll1l_opy_+bstack1l11l1l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᓢ"), bstack1ll1ll1ll1l_opy_+bstack1l11l1l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᓣ"), True, None)
            if bstack1l11lllllll_opy_ == bstack1111l11l11_opy_.PRE and callable(bstack1l1l1111l11_opy_):
                return bstack1l1l1111l11_opy_
            elif bstack1l11lllllll_opy_ == bstack1111l11l11_opy_.POST and bstack1l1l1111l11_opy_:
                return bstack1l1l1111l11_opy_
    def bstack11111l1ll1_opy_(
        self, method_name, previous_state: bstack111111l11l_opy_, *args, **kwargs
    ) -> bstack111111l11l_opy_:
        if method_name == bstack1l11l1l_opy_ (u"ࠢࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠࠤᓤ") or method_name == bstack1l11l1l_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᓥ"):
            return bstack111111l11l_opy_.bstack1111l1l111_opy_
        if method_name == bstack1l11l1l_opy_ (u"ࠤࡴࡹ࡮ࡺࠢᓦ"):
            return bstack111111l11l_opy_.QUIT
        if method_name == bstack1l11l1l_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᓧ"):
            if previous_state != bstack111111l11l_opy_.NONE:
                bstack1ll11lll1ll_opy_ = bstack1llll11lll1_opy_.bstack1l1l11l111l_opy_(*args)
                if bstack1ll11lll1ll_opy_ == bstack1llll11lll1_opy_.bstack1l1l1l11lll_opy_:
                    return bstack111111l11l_opy_.bstack1111l1l111_opy_
            return bstack111111l11l_opy_.bstack111111lll1_opy_
        return bstack111111l11l_opy_.NONE