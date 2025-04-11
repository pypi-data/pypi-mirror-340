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
import threading
class bstack11l1l1111l_opy_(threading.Thread):
    def run(self):
        self.exc = None
        try:
            self.ret = self._target(*self._args, **self._kwargs)
        except Exception as e:
            self.exc = e
    def join(self, timeout=None):
        super(bstack11l1l1111l_opy_, self).join(timeout)
        if self.exc:
            raise self.exc
        return self.ret