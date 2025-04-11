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
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack111lll111_opy_():
  def __init__(self, args, logger, bstack1111llllll_opy_, bstack1111lll11l_opy_, bstack1111ll1l1l_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111llllll_opy_ = bstack1111llllll_opy_
    self.bstack1111lll11l_opy_ = bstack1111lll11l_opy_
    self.bstack1111ll1l1l_opy_ = bstack1111ll1l1l_opy_
  def bstack1llll111ll_opy_(self, bstack111l1111ll_opy_, bstack11l11ll1l1_opy_, bstack1111ll1ll1_opy_=False):
    bstack1l1lll1l_opy_ = []
    manager = multiprocessing.Manager()
    bstack1111lll111_opy_ = manager.list()
    bstack1llll1l1l_opy_ = Config.bstack11ll1l11l_opy_()
    if bstack1111ll1ll1_opy_:
      for index, platform in enumerate(self.bstack1111llllll_opy_[bstack1l11l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩစ")]):
        if index == 0:
          bstack11l11ll1l1_opy_[bstack1l11l1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪဆ")] = self.args
        bstack1l1lll1l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack111l1111ll_opy_,
                                                    args=(bstack11l11ll1l1_opy_, bstack1111lll111_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111llllll_opy_[bstack1l11l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫဇ")]):
        bstack1l1lll1l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack111l1111ll_opy_,
                                                    args=(bstack11l11ll1l1_opy_, bstack1111lll111_opy_)))
    i = 0
    for t in bstack1l1lll1l_opy_:
      try:
        if bstack1llll1l1l_opy_.get_property(bstack1l11l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪဈ")):
          os.environ[bstack1l11l1l_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫဉ")] = json.dumps(self.bstack1111llllll_opy_[bstack1l11l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧည")][i % self.bstack1111ll1l1l_opy_])
      except Exception as e:
        self.logger.debug(bstack1l11l1l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡹࡵࡲࡪࡰࡪࠤࡨࡻࡲࡳࡧࡱࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡧࡷࡥ࡮ࡲࡳ࠻ࠢࡾࢁࠧဋ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1l1lll1l_opy_:
      t.join()
    return list(bstack1111lll111_opy_)