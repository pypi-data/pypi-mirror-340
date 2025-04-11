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
from collections import deque
from bstack_utils.constants import *
class bstack11l11ll111_opy_:
    def __init__(self):
        self._111ll11l111_opy_ = deque()
        self._111ll11llll_opy_ = {}
        self._111ll11ll11_opy_ = False
    def bstack111ll11l11l_opy_(self, test_name, bstack111ll11l1l1_opy_):
        bstack111ll111l1l_opy_ = self._111ll11llll_opy_.get(test_name, {})
        return bstack111ll111l1l_opy_.get(bstack111ll11l1l1_opy_, 0)
    def bstack111ll11ll1l_opy_(self, test_name, bstack111ll11l1l1_opy_):
        bstack111ll1111ll_opy_ = self.bstack111ll11l11l_opy_(test_name, bstack111ll11l1l1_opy_)
        self.bstack111ll11l1ll_opy_(test_name, bstack111ll11l1l1_opy_)
        return bstack111ll1111ll_opy_
    def bstack111ll11l1ll_opy_(self, test_name, bstack111ll11l1l1_opy_):
        if test_name not in self._111ll11llll_opy_:
            self._111ll11llll_opy_[test_name] = {}
        bstack111ll111l1l_opy_ = self._111ll11llll_opy_[test_name]
        bstack111ll1111ll_opy_ = bstack111ll111l1l_opy_.get(bstack111ll11l1l1_opy_, 0)
        bstack111ll111l1l_opy_[bstack111ll11l1l1_opy_] = bstack111ll1111ll_opy_ + 1
    def bstack111lll11l_opy_(self, bstack111ll111lll_opy_, bstack111ll11lll1_opy_):
        bstack111ll111ll1_opy_ = self.bstack111ll11ll1l_opy_(bstack111ll111lll_opy_, bstack111ll11lll1_opy_)
        event_name = bstack11lll1111l1_opy_[bstack111ll11lll1_opy_]
        bstack1l1ll1ll1ll_opy_ = bstack1l11l1l_opy_ (u"ࠢࡼࡿ࠰ࡿࢂ࠳ࡻࡾࠤ᳧").format(bstack111ll111lll_opy_, event_name, bstack111ll111ll1_opy_)
        self._111ll11l111_opy_.append(bstack1l1ll1ll1ll_opy_)
    def bstack1ll1l1ll1l_opy_(self):
        return len(self._111ll11l111_opy_) == 0
    def bstack1ll11l11l_opy_(self):
        bstack111ll111l11_opy_ = self._111ll11l111_opy_.popleft()
        return bstack111ll111l11_opy_
    def capturing(self):
        return self._111ll11ll11_opy_
    def bstack111ll111_opy_(self):
        self._111ll11ll11_opy_ = True
    def bstack111ll11l_opy_(self):
        self._111ll11ll11_opy_ = False