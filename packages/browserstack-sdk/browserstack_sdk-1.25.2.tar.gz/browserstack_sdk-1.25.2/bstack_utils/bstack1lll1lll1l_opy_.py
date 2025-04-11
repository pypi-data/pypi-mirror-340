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
class bstack111llll1_opy_:
    def __init__(self, handler):
        self._111l11l11ll_opy_ = None
        self.handler = handler
        self._111l11l11l1_opy_ = self.bstack111l11l1111_opy_()
        self.patch()
    def patch(self):
        self._111l11l11ll_opy_ = self._111l11l11l1_opy_.execute
        self._111l11l11l1_opy_.execute = self.bstack111l11l111l_opy_()
    def bstack111l11l111l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l11l1l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࠦᵰ"), driver_command, None, this, args)
            response = self._111l11l11ll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l11l1l_opy_ (u"ࠧࡧࡦࡵࡧࡵࠦᵱ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._111l11l11l1_opy_.execute = self._111l11l11ll_opy_
    @staticmethod
    def bstack111l11l1111_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver