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
from browserstack_sdk.sdk_cli.bstack1lll1ll1111_opy_ import bstack1lll11l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack111111l1l1_opy_ import (
    bstack111111l11l_opy_,
    bstack1111l11l11_opy_,
    bstack1llllllllll_opy_,
    bstack1111l11lll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll111l1ll_opy_ import bstack1llll11lll1_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1l11_opy_ import bstack1llll1111ll_opy_
from browserstack_sdk.sdk_cli.bstack111111111l_opy_ import bstack11111ll1l1_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1lll1ll1111_opy_ import bstack1lll11l1ll1_opy_
import weakref
class bstack1ll11l11l11_opy_(bstack1lll11l1ll1_opy_):
    bstack1ll11l111ll_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1111l11lll_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1111l11lll_opy_]]
    def __init__(self, bstack1ll11l111ll_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1ll11l1l111_opy_ = dict()
        self.bstack1ll11l111ll_opy_ = bstack1ll11l111ll_opy_
        self.frameworks = frameworks
        bstack1llll1111ll_opy_.bstack1ll1lll111l_opy_((bstack111111l11l_opy_.bstack1111l1l111_opy_, bstack1111l11l11_opy_.POST), self.__1ll11l1l1l1_opy_)
        if any(bstack1llll11lll1_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1llll11lll1_opy_.bstack1ll1lll111l_opy_(
                (bstack111111l11l_opy_.bstack111111lll1_opy_, bstack1111l11l11_opy_.PRE), self.__1ll11l1ll11_opy_
            )
            bstack1llll11lll1_opy_.bstack1ll1lll111l_opy_(
                (bstack111111l11l_opy_.QUIT, bstack1111l11l11_opy_.POST), self.__1ll11l11lll_opy_
            )
    def __1ll11l1l1l1_opy_(
        self,
        f: bstack1llll1111ll_opy_,
        bstack1ll11l1l1ll_opy_: object,
        exec: Tuple[bstack1111l11lll_opy_, str],
        bstack1llllllll1l_opy_: Tuple[bstack111111l11l_opy_, bstack1111l11l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1l11l1l_opy_ (u"ࠥࡲࡪࡽ࡟ࡱࡣࡪࡩࠧᆟ"):
                return
            contexts = bstack1ll11l1l1ll_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1l11l1l_opy_ (u"ࠦࡦࡨ࡯ࡶࡶ࠽ࡦࡱࡧ࡮࡬ࠤᆠ") in page.url:
                                self.logger.debug(bstack1l11l1l_opy_ (u"࡙ࠧࡴࡰࡴ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡲࡪࡽࠠࡱࡣࡪࡩࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠢᆡ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1llllllllll_opy_.bstack11111l1111_opy_(instance, self.bstack1ll11l111ll_opy_, True)
                                self.logger.debug(bstack1l11l1l_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡵࡧࡧࡦࡡ࡬ࡲ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᆢ") + str(instance.ref()) + bstack1l11l1l_opy_ (u"ࠢࠣᆣ"))
        except Exception as e:
            self.logger.debug(bstack1l11l1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡰࡨࡻࠥࡶࡡࡨࡧࠣ࠾ࠧᆤ"),e)
    def __1ll11l1ll11_opy_(
        self,
        f: bstack1llll11lll1_opy_,
        driver: object,
        exec: Tuple[bstack1111l11lll_opy_, str],
        bstack1llllllll1l_opy_: Tuple[bstack111111l11l_opy_, bstack1111l11l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1llllllllll_opy_.bstack1111l11111_opy_(instance, self.bstack1ll11l111ll_opy_, False):
            return
        if not f.bstack1ll11ll1l11_opy_(f.hub_url(driver)):
            self.bstack1ll11l1l111_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1llllllllll_opy_.bstack11111l1111_opy_(instance, self.bstack1ll11l111ll_opy_, True)
            self.logger.debug(bstack1l11l1l_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡ࡬ࡲ࡮ࡺ࠺ࠡࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡩࡸࡩࡷࡧࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᆥ") + str(instance.ref()) + bstack1l11l1l_opy_ (u"ࠥࠦᆦ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1llllllllll_opy_.bstack11111l1111_opy_(instance, self.bstack1ll11l111ll_opy_, True)
        self.logger.debug(bstack1l11l1l_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࡣ࡮ࡴࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᆧ") + str(instance.ref()) + bstack1l11l1l_opy_ (u"ࠧࠨᆨ"))
    def __1ll11l11lll_opy_(
        self,
        f: bstack1llll11lll1_opy_,
        driver: object,
        exec: Tuple[bstack1111l11lll_opy_, str],
        bstack1llllllll1l_opy_: Tuple[bstack111111l11l_opy_, bstack1111l11l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1ll11l11ll1_opy_(instance)
        self.logger.debug(bstack1l11l1l_opy_ (u"ࠨ࡟ࡠࡱࡱࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡱࡶ࡫ࡷ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᆩ") + str(instance.ref()) + bstack1l11l1l_opy_ (u"ࠢࠣᆪ"))
    def bstack1ll11l11l1l_opy_(self, context: bstack11111ll1l1_opy_, reverse=True) -> List[Tuple[Callable, bstack1111l11lll_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1ll11l1llll_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1llll11lll1_opy_.bstack1ll1l1l1ll1_opy_(data[1])
                    and data[1].bstack1ll11l1llll_opy_(context)
                    and getattr(data[0](), bstack1l11l1l_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧᆫ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1111111l11_opy_, reverse=reverse)
    def bstack1ll11l1l11l_opy_(self, context: bstack11111ll1l1_opy_, reverse=True) -> List[Tuple[Callable, bstack1111l11lll_opy_]]:
        matches = []
        for data in self.bstack1ll11l1l111_opy_.values():
            if (
                data[1].bstack1ll11l1llll_opy_(context)
                and getattr(data[0](), bstack1l11l1l_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᆬ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1111111l11_opy_, reverse=reverse)
    def bstack1ll11l1ll1l_opy_(self, instance: bstack1111l11lll_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1ll11l11ll1_opy_(self, instance: bstack1111l11lll_opy_) -> bool:
        if self.bstack1ll11l1ll1l_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1llllllllll_opy_.bstack11111l1111_opy_(instance, self.bstack1ll11l111ll_opy_, False)
            return True
        return False