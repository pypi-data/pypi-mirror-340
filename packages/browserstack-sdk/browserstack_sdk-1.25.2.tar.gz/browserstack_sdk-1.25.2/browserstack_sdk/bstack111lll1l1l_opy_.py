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
class RobotHandler():
    def __init__(self, args, logger, bstack1111llllll_opy_, bstack1111lll11l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111llllll_opy_ = bstack1111llllll_opy_
        self.bstack1111lll11l_opy_ = bstack1111lll11l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111lll11l1_opy_(bstack1111ll11ll_opy_):
        bstack1111ll1l11_opy_ = []
        if bstack1111ll11ll_opy_:
            tokens = str(os.path.basename(bstack1111ll11ll_opy_)).split(bstack1l11l1l_opy_ (u"ࠨ࡟ࠣဌ"))
            camelcase_name = bstack1l11l1l_opy_ (u"ࠢࠡࠤဍ").join(t.title() for t in tokens)
            suite_name, bstack1111ll111l_opy_ = os.path.splitext(camelcase_name)
            bstack1111ll1l11_opy_.append(suite_name)
        return bstack1111ll1l11_opy_
    @staticmethod
    def bstack1111ll11l1_opy_(typename):
        if bstack1l11l1l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦဎ") in typename:
            return bstack1l11l1l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥဏ")
        return bstack1l11l1l_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦတ")