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
import abc
from browserstack_sdk.sdk_cli.bstack1111l1llll_opy_ import bstack1111l1lll1_opy_
class bstack1lll11l1ll1_opy_(abc.ABC):
    bin_session_id: str
    bstack1111l1llll_opy_: bstack1111l1lll1_opy_
    def __init__(self):
        self.bstack1lll11ll1ll_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1111l1llll_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1llll1111l1_opy_(self):
        return (self.bstack1lll11ll1ll_opy_ != None and self.bin_session_id != None and self.bstack1111l1llll_opy_ != None)
    def configure(self, bstack1lll11ll1ll_opy_, config, bin_session_id: str, bstack1111l1llll_opy_: bstack1111l1lll1_opy_):
        self.bstack1lll11ll1ll_opy_ = bstack1lll11ll1ll_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1111l1llll_opy_ = bstack1111l1llll_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1l11l1l_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡦࡦࠣࡱࡴࡪࡵ࡭ࡧࠣࡿࡸ࡫࡬ࡧ࠰ࡢࡣࡨࡲࡡࡴࡵࡢࡣ࠳ࡥ࡟࡯ࡣࡰࡩࡤࡥࡽ࠻ࠢࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࡀࠦᆜ") + str(self.bin_session_id) + bstack1l11l1l_opy_ (u"ࠣࠤᆝ"))
    def bstack1ll1l1ll1ll_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1l11l1l_opy_ (u"ࠤࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠣࡧࡦࡴ࡮ࡰࡶࠣࡦࡪࠦࡎࡰࡰࡨࠦᆞ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False