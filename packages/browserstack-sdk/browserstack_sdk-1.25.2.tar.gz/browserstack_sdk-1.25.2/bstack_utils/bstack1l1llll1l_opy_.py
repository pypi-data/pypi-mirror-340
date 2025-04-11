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
import json
from bstack_utils.bstack1l111l1ll_opy_ import get_logger
logger = get_logger(__name__)
class bstack11lll1ll111_opy_(object):
  bstack1l11l11l_opy_ = os.path.join(os.path.expanduser(bstack1l11l1l_opy_ (u"ࠫࢃ࠭ᘪ")), bstack1l11l1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᘫ"))
  bstack11lll1l1lll_opy_ = os.path.join(bstack1l11l11l_opy_, bstack1l11l1l_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳ࠯࡬ࡶࡳࡳ࠭ᘬ"))
  commands_to_wrap = None
  perform_scan = None
  bstack11ll1ll11l_opy_ = None
  bstack111l11l11_opy_ = None
  bstack11lllll111l_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l11l1l_opy_ (u"ࠧࡪࡰࡶࡸࡦࡴࡣࡦࠩᘭ")):
      cls.instance = super(bstack11lll1ll111_opy_, cls).__new__(cls)
      cls.instance.bstack11lll1ll1l1_opy_()
    return cls.instance
  def bstack11lll1ll1l1_opy_(self):
    try:
      with open(self.bstack11lll1l1lll_opy_, bstack1l11l1l_opy_ (u"ࠨࡴࠪᘮ")) as bstack1lllll1ll1_opy_:
        bstack11lll1ll11l_opy_ = bstack1lllll1ll1_opy_.read()
        data = json.loads(bstack11lll1ll11l_opy_)
        if bstack1l11l1l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᘯ") in data:
          self.bstack11lllll1l1l_opy_(data[bstack1l11l1l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬᘰ")])
        if bstack1l11l1l_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬᘱ") in data:
          self.bstack11ll1l1l1_opy_(data[bstack1l11l1l_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ᘲ")])
    except:
      pass
  def bstack11ll1l1l1_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1l11l1l_opy_ (u"࠭ࡳࡤࡣࡱࠫᘳ"),bstack1l11l1l_opy_ (u"ࠧࠨᘴ"))
      self.bstack11ll1ll11l_opy_ = scripts.get(bstack1l11l1l_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠬᘵ"),bstack1l11l1l_opy_ (u"ࠩࠪᘶ"))
      self.bstack111l11l11_opy_ = scripts.get(bstack1l11l1l_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧᘷ"),bstack1l11l1l_opy_ (u"ࠫࠬᘸ"))
      self.bstack11lllll111l_opy_ = scripts.get(bstack1l11l1l_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪᘹ"),bstack1l11l1l_opy_ (u"࠭ࠧᘺ"))
  def bstack11lllll1l1l_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11lll1l1lll_opy_, bstack1l11l1l_opy_ (u"ࠧࡸࠩᘻ")) as file:
        json.dump({
          bstack1l11l1l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࠥᘼ"): self.commands_to_wrap,
          bstack1l11l1l_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࡵࠥᘽ"): {
            bstack1l11l1l_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᘾ"): self.perform_scan,
            bstack1l11l1l_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣᘿ"): self.bstack11ll1ll11l_opy_,
            bstack1l11l1l_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠤᙀ"): self.bstack111l11l11_opy_,
            bstack1l11l1l_opy_ (u"ࠨࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠦᙁ"): self.bstack11lllll111l_opy_
          }
        }, file)
    except Exception as e:
      logger.error(bstack1l11l1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰࡥࡳࡪࡳ࠻ࠢࡾࢁࠧᙂ").format(e))
      pass
  def bstack11l11llll_opy_(self, bstack1ll11lll1ll_opy_):
    try:
      return any(command.get(bstack1l11l1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᙃ")) == bstack1ll11lll1ll_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack1l1llll1l_opy_ = bstack11lll1ll111_opy_()