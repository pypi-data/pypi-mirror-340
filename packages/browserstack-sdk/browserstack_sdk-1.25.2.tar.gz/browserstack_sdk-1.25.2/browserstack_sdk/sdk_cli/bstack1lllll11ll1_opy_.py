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
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll1ll1111_opy_ import bstack1lll11l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack111111l1l1_opy_ import (
    bstack111111l11l_opy_,
    bstack1111l11l11_opy_,
    bstack1111l11lll_opy_,
)
from bstack_utils.helper import  bstack111l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll111l1ll_opy_ import bstack1llll11lll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lllll11l11_opy_, bstack1lll1l11l1l_opy_, bstack1lll11111ll_opy_, bstack1lll1l1ll1l_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1l1l1lll_opy_ import bstack11l11ll111_opy_
from browserstack_sdk.sdk_cli.bstack1llllll11l1_opy_ import bstack1lll11l1111_opy_
from bstack_utils.percy import bstack1l11ll1l_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1llll1l1l11_opy_(bstack1lll11l1ll1_opy_):
    def __init__(self, bstack1l1ll1ll111_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1ll1ll111_opy_ = bstack1l1ll1ll111_opy_
        self.percy = bstack1l11ll1l_opy_()
        self.bstack1l1ll1ll1_opy_ = bstack11l11ll111_opy_()
        self.bstack1l1ll1lll11_opy_()
        bstack1llll11lll1_opy_.bstack1ll1lll111l_opy_((bstack111111l11l_opy_.bstack111111lll1_opy_, bstack1111l11l11_opy_.PRE), self.bstack1l1ll1l1lll_opy_)
        TestFramework.bstack1ll1lll111l_opy_((bstack1lllll11l11_opy_.TEST, bstack1lll11111ll_opy_.POST), self.bstack1ll1l11l1ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1111ll11_opy_(self, instance: bstack1111l11lll_opy_, driver: object):
        bstack1l1llll1l11_opy_ = TestFramework.bstack11111ll1ll_opy_(instance.context)
        for t in bstack1l1llll1l11_opy_:
            bstack1l1lll1l1ll_opy_ = TestFramework.bstack1111l11111_opy_(t, bstack1lll11l1111_opy_.bstack1ll1111lll1_opy_, [])
            if any(instance is d[1] for d in bstack1l1lll1l1ll_opy_) or instance == driver:
                return t
    def bstack1l1ll1l1lll_opy_(
        self,
        f: bstack1llll11lll1_opy_,
        driver: object,
        exec: Tuple[bstack1111l11lll_opy_, str],
        bstack1llllllll1l_opy_: Tuple[bstack111111l11l_opy_, bstack1111l11l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1llll11lll1_opy_.bstack1ll1ll1l1l1_opy_(method_name):
                return
            platform_index = f.bstack1111l11111_opy_(instance, bstack1llll11lll1_opy_.bstack1ll1l11l111_opy_, 0)
            bstack1l1llll1111_opy_ = self.bstack1ll1111ll11_opy_(instance, driver)
            bstack1l1ll1ll1ll_opy_ = TestFramework.bstack1111l11111_opy_(bstack1l1llll1111_opy_, TestFramework.bstack1l1ll1l1l11_opy_, None)
            if not bstack1l1ll1ll1ll_opy_:
                self.logger.debug(bstack1l11l1l_opy_ (u"ࠣࡱࡱࡣࡵࡸࡥࡠࡧࡻࡩࡨࡻࡴࡦ࠼ࠣࡶࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡡࡴࠢࡶࡩࡸࡹࡩࡰࡰࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡽࡪࡺࠠࡴࡶࡤࡶࡹ࡫ࡤࠣሩ"))
                return
            driver_command = f.bstack1ll11llll1l_opy_(*args)
            for command in bstack11lll11ll_opy_:
                if command == driver_command:
                    self.bstack11llllll1_opy_(driver, platform_index)
            bstack1l11l111l_opy_ = self.percy.bstack1lll11lll1_opy_()
            if driver_command in bstack11lll11lll_opy_[bstack1l11l111l_opy_]:
                self.bstack1l1ll1ll1_opy_.bstack111lll11l_opy_(bstack1l1ll1ll1ll_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1l11l1l_opy_ (u"ࠤࡲࡲࡤࡶࡲࡦࡡࡨࡼࡪࡩࡵࡵࡧ࠽ࠤࡪࡸࡲࡰࡴࠥሪ"), e)
    def bstack1ll1l11l1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l11l1l_opy_,
        bstack1llllllll1l_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll11111ll_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1111l11l_opy_ import bstack1lllll11l1l_opy_
        bstack1l1lll1l1ll_opy_ = f.bstack1111l11111_opy_(instance, bstack1lll11l1111_opy_.bstack1ll1111lll1_opy_, [])
        if not bstack1l1lll1l1ll_opy_:
            self.logger.debug(bstack1l11l1l_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧራ") + str(kwargs) + bstack1l11l1l_opy_ (u"ࠦࠧሬ"))
            return
        if len(bstack1l1lll1l1ll_opy_) > 1:
            self.logger.debug(bstack1l11l1l_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢር") + str(kwargs) + bstack1l11l1l_opy_ (u"ࠨࠢሮ"))
        bstack1l1ll1l11ll_opy_, bstack1l1ll1llll1_opy_ = bstack1l1lll1l1ll_opy_[0]
        driver = bstack1l1ll1l11ll_opy_()
        if not driver:
            self.logger.debug(bstack1l11l1l_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣሯ") + str(kwargs) + bstack1l11l1l_opy_ (u"ࠣࠤሰ"))
            return
        bstack1l1ll1ll1l1_opy_ = {
            TestFramework.bstack1ll1l11ll11_opy_: bstack1l11l1l_opy_ (u"ࠤࡷࡩࡸࡺࠠ࡯ࡣࡰࡩࠧሱ"),
            TestFramework.bstack1ll1l1111l1_opy_: bstack1l11l1l_opy_ (u"ࠥࡸࡪࡹࡴࠡࡷࡸ࡭ࡩࠨሲ"),
            TestFramework.bstack1l1ll1l1l11_opy_: bstack1l11l1l_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡵࡩࡷࡻ࡮ࠡࡰࡤࡱࡪࠨሳ")
        }
        bstack1l1ll1l11l1_opy_ = { key: f.bstack1111l11111_opy_(instance, key) for key in bstack1l1ll1ll1l1_opy_ }
        bstack1l1ll1l1l1l_opy_ = [key for key, value in bstack1l1ll1l11l1_opy_.items() if not value]
        if bstack1l1ll1l1l1l_opy_:
            for key in bstack1l1ll1l1l1l_opy_:
                self.logger.debug(bstack1l11l1l_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠣሴ") + str(key) + bstack1l11l1l_opy_ (u"ࠨࠢስ"))
            return
        platform_index = f.bstack1111l11111_opy_(instance, bstack1llll11lll1_opy_.bstack1ll1l11l111_opy_, 0)
        if self.bstack1l1ll1ll111_opy_.percy_capture_mode == bstack1l11l1l_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤሶ"):
            bstack1111ll1l1_opy_ = bstack1l1ll1l11l1_opy_.get(TestFramework.bstack1l1ll1l1l11_opy_) + bstack1l11l1l_opy_ (u"ࠣ࠯ࡷࡩࡸࡺࡣࡢࡵࡨࠦሷ")
            bstack1ll1ll1ll1l_opy_ = bstack1lllll11l1l_opy_.bstack1ll11llll11_opy_(EVENTS.bstack1l1ll1l1ll1_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1111ll1l1_opy_,
                bstack1lll11ll1l_opy_=bstack1l1ll1l11l1_opy_[TestFramework.bstack1ll1l11ll11_opy_],
                bstack1l111l1l11_opy_=bstack1l1ll1l11l1_opy_[TestFramework.bstack1ll1l1111l1_opy_],
                bstack11l11111l_opy_=platform_index
            )
            bstack1lllll11l1l_opy_.end(EVENTS.bstack1l1ll1l1ll1_opy_.value, bstack1ll1ll1ll1l_opy_+bstack1l11l1l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤሸ"), bstack1ll1ll1ll1l_opy_+bstack1l11l1l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣሹ"), True, None, None, None, None, test_name=bstack1111ll1l1_opy_)
    def bstack11llllll1_opy_(self, driver, platform_index):
        if self.bstack1l1ll1ll1_opy_.bstack1ll1l1ll1l_opy_() is True or self.bstack1l1ll1ll1_opy_.capturing() is True:
            return
        self.bstack1l1ll1ll1_opy_.bstack111ll111_opy_()
        while not self.bstack1l1ll1ll1_opy_.bstack1ll1l1ll1l_opy_():
            bstack1l1ll1ll1ll_opy_ = self.bstack1l1ll1ll1_opy_.bstack1ll11l11l_opy_()
            self.bstack1ll111ll11_opy_(driver, bstack1l1ll1ll1ll_opy_, platform_index)
        self.bstack1l1ll1ll1_opy_.bstack111ll11l_opy_()
    def bstack1ll111ll11_opy_(self, driver, bstack1111l11ll_opy_, platform_index, test=None):
        from bstack_utils.bstack1111l11l_opy_ import bstack1lllll11l1l_opy_
        bstack1ll1ll1ll1l_opy_ = bstack1lllll11l1l_opy_.bstack1ll11llll11_opy_(EVENTS.bstack1ll1l1111_opy_.value)
        if test != None:
            bstack1lll11ll1l_opy_ = getattr(test, bstack1l11l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩሺ"), None)
            bstack1l111l1l11_opy_ = getattr(test, bstack1l11l1l_opy_ (u"ࠬࡻࡵࡪࡦࠪሻ"), None)
            PercySDK.screenshot(driver, bstack1111l11ll_opy_, bstack1lll11ll1l_opy_=bstack1lll11ll1l_opy_, bstack1l111l1l11_opy_=bstack1l111l1l11_opy_, bstack11l11111l_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1111l11ll_opy_)
        bstack1lllll11l1l_opy_.end(EVENTS.bstack1ll1l1111_opy_.value, bstack1ll1ll1ll1l_opy_+bstack1l11l1l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨሼ"), bstack1ll1ll1ll1l_opy_+bstack1l11l1l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧሽ"), True, None, None, None, None, test_name=bstack1111l11ll_opy_)
    def bstack1l1ll1lll11_opy_(self):
        os.environ[bstack1l11l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞࠭ሾ")] = str(self.bstack1l1ll1ll111_opy_.success)
        os.environ[bstack1l11l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭ሿ")] = str(self.bstack1l1ll1ll111_opy_.percy_capture_mode)
        self.percy.bstack1l1ll1lll1l_opy_(self.bstack1l1ll1ll111_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1ll1ll11l_opy_(self.bstack1l1ll1ll111_opy_.percy_build_id)