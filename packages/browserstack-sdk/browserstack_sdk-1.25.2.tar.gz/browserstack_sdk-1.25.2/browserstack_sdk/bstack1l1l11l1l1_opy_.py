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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.accessibility as bstack1l1lll11ll_opy_
from browserstack_sdk.bstack1l1lll1ll1_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l1l1lll1_opy_
class bstack1lll1l111l_opy_:
    def __init__(self, args, logger, bstack1111llllll_opy_, bstack1111lll11l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111llllll_opy_ = bstack1111llllll_opy_
        self.bstack1111lll11l_opy_ = bstack1111lll11l_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11l1l1ll11_opy_ = []
        self.bstack111l111l1l_opy_ = None
        self.bstack1lll11111l_opy_ = []
        self.bstack1111lllll1_opy_ = self.bstack11lll11l11_opy_()
        self.bstack1ll1ll11l1_opy_ = -1
    def bstack11l11ll1l1_opy_(self, bstack111l111111_opy_):
        self.parse_args()
        self.bstack1111llll1l_opy_()
        self.bstack1111ll1lll_opy_(bstack111l111111_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1111lll1ll_opy_():
        import importlib
        if getattr(importlib, bstack1l11l1l_opy_ (u"ࠩࡩ࡭ࡳࡪ࡟࡭ࡱࡤࡨࡪࡸࠧ࿥"), False):
            bstack111l111lll_opy_ = importlib.find_loader(bstack1l11l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠬ࿦"))
        else:
            bstack111l111lll_opy_ = importlib.util.find_spec(bstack1l11l1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭࿧"))
    def bstack111l11111l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1ll1ll11l1_opy_ = -1
        if self.bstack1111lll11l_opy_ and bstack1l11l1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ࿨") in self.bstack1111llllll_opy_:
            self.bstack1ll1ll11l1_opy_ = int(self.bstack1111llllll_opy_[bstack1l11l1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭࿩")])
        try:
            bstack1111llll11_opy_ = [bstack1l11l1l_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩ࿪"), bstack1l11l1l_opy_ (u"ࠨ࠯࠰ࡴࡱࡻࡧࡪࡰࡶࠫ࿫"), bstack1l11l1l_opy_ (u"ࠩ࠰ࡴࠬ࿬")]
            if self.bstack1ll1ll11l1_opy_ >= 0:
                bstack1111llll11_opy_.extend([bstack1l11l1l_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ࿭"), bstack1l11l1l_opy_ (u"ࠫ࠲ࡴࠧ࿮")])
            for arg in bstack1111llll11_opy_:
                self.bstack111l11111l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1111llll1l_opy_(self):
        bstack111l111l1l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack111l111l1l_opy_ = bstack111l111l1l_opy_
        return bstack111l111l1l_opy_
    def bstack1ll11111_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack1111lll1ll_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l1l1lll1_opy_)
    def bstack1111ll1lll_opy_(self, bstack111l111111_opy_):
        bstack1llll1l1l_opy_ = Config.bstack11ll1l11l_opy_()
        if bstack111l111111_opy_:
            self.bstack111l111l1l_opy_.append(bstack1l11l1l_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ࿯"))
            self.bstack111l111l1l_opy_.append(bstack1l11l1l_opy_ (u"࠭ࡔࡳࡷࡨࠫ࿰"))
        if bstack1llll1l1l_opy_.bstack111l11l111_opy_():
            self.bstack111l111l1l_opy_.append(bstack1l11l1l_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭࿱"))
            self.bstack111l111l1l_opy_.append(bstack1l11l1l_opy_ (u"ࠨࡖࡵࡹࡪ࠭࿲"))
        self.bstack111l111l1l_opy_.append(bstack1l11l1l_opy_ (u"ࠩ࠰ࡴࠬ࿳"))
        self.bstack111l111l1l_opy_.append(bstack1l11l1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠨ࿴"))
        self.bstack111l111l1l_opy_.append(bstack1l11l1l_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭࿵"))
        self.bstack111l111l1l_opy_.append(bstack1l11l1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ࿶"))
        if self.bstack1ll1ll11l1_opy_ > 1:
            self.bstack111l111l1l_opy_.append(bstack1l11l1l_opy_ (u"࠭࠭࡯ࠩ࿷"))
            self.bstack111l111l1l_opy_.append(str(self.bstack1ll1ll11l1_opy_))
    def bstack111l1111l1_opy_(self):
        bstack1lll11111l_opy_ = []
        for spec in self.bstack11l1l1ll11_opy_:
            bstack1l1l111l1l_opy_ = [spec]
            bstack1l1l111l1l_opy_ += self.bstack111l111l1l_opy_
            bstack1lll11111l_opy_.append(bstack1l1l111l1l_opy_)
        self.bstack1lll11111l_opy_ = bstack1lll11111l_opy_
        return bstack1lll11111l_opy_
    def bstack11lll11l11_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1111lllll1_opy_ = True
            return True
        except Exception as e:
            self.bstack1111lllll1_opy_ = False
        return self.bstack1111lllll1_opy_
    def bstack1llll111ll_opy_(self, bstack111l1111ll_opy_, bstack11l11ll1l1_opy_):
        bstack11l11ll1l1_opy_[bstack1l11l1l_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧ࿸")] = self.bstack1111llllll_opy_
        multiprocessing.set_start_method(bstack1l11l1l_opy_ (u"ࠨࡵࡳࡥࡼࡴࠧ࿹"))
        bstack1l1lll1l_opy_ = []
        manager = multiprocessing.Manager()
        bstack1111lll111_opy_ = manager.list()
        if bstack1l11l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ࿺") in self.bstack1111llllll_opy_:
            for index, platform in enumerate(self.bstack1111llllll_opy_[bstack1l11l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭࿻")]):
                bstack1l1lll1l_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack111l1111ll_opy_,
                                                            args=(self.bstack111l111l1l_opy_, bstack11l11ll1l1_opy_, bstack1111lll111_opy_)))
            bstack111l111ll1_opy_ = len(self.bstack1111llllll_opy_[bstack1l11l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ࿼")])
        else:
            bstack1l1lll1l_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack111l1111ll_opy_,
                                                        args=(self.bstack111l111l1l_opy_, bstack11l11ll1l1_opy_, bstack1111lll111_opy_)))
            bstack111l111ll1_opy_ = 1
        i = 0
        for t in bstack1l1lll1l_opy_:
            os.environ[bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ࿽")] = str(i)
            if bstack1l11l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ࿾") in self.bstack1111llllll_opy_:
                os.environ[bstack1l11l1l_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨ࿿")] = json.dumps(self.bstack1111llllll_opy_[bstack1l11l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫက")][i % bstack111l111ll1_opy_])
            i += 1
            t.start()
        for t in bstack1l1lll1l_opy_:
            t.join()
        return list(bstack1111lll111_opy_)
    @staticmethod
    def bstack11l1111l1_opy_(driver, bstack111l111l11_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ခ"), None)
        if item and getattr(item, bstack1l11l1l_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࠬဂ"), None) and not getattr(item, bstack1l11l1l_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࡠࡦࡲࡲࡪ࠭ဃ"), False):
            logger.info(
                bstack1l11l1l_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠦင"))
            bstack1111lll1l1_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1l1lll11ll_opy_.bstack11ll1lll11_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)