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
import logging
import datetime
import threading
from bstack_utils.helper import bstack11lllll11l1_opy_, bstack1ll11l1l1l_opy_, get_host_info, bstack11l1ll1ll1l_opy_, \
 bstack1l11l1l111_opy_, bstack111l1ll1_opy_, bstack111l11l11l_opy_, bstack11l1l11l1l1_opy_, bstack1l1ll1l1l_opy_
import bstack_utils.accessibility as bstack1l1lll11ll_opy_
from bstack_utils.bstack11l111111l_opy_ import bstack111ll111l_opy_
from bstack_utils.percy import bstack1l11ll1l_opy_
from bstack_utils.config import Config
bstack1llll1l1l_opy_ = Config.bstack11ll1l11l_opy_()
logger = logging.getLogger(__name__)
percy = bstack1l11ll1l_opy_()
@bstack111l11l11l_opy_(class_method=False)
def bstack1111lll1lll_opy_(bs_config, bstack1l1ll111l_opy_):
  try:
    data = {
        bstack1l11l1l_opy_ (u"ࠩࡩࡳࡷࡳࡡࡵࠩỡ"): bstack1l11l1l_opy_ (u"ࠪ࡮ࡸࡵ࡮ࠨỢ"),
        bstack1l11l1l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡤࡴࡡ࡮ࡧࠪợ"): bs_config.get(bstack1l11l1l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪỤ"), bstack1l11l1l_opy_ (u"࠭ࠧụ")),
        bstack1l11l1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬỦ"): bs_config.get(bstack1l11l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫủ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l11l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬỨ"): bs_config.get(bstack1l11l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬứ")),
        bstack1l11l1l_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩỪ"): bs_config.get(bstack1l11l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨừ"), bstack1l11l1l_opy_ (u"࠭ࠧỬ")),
        bstack1l11l1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫử"): bstack1l1ll1l1l_opy_(),
        bstack1l11l1l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭Ữ"): bstack11l1ll1ll1l_opy_(bs_config),
        bstack1l11l1l_opy_ (u"ࠩ࡫ࡳࡸࡺ࡟ࡪࡰࡩࡳࠬữ"): get_host_info(),
        bstack1l11l1l_opy_ (u"ࠪࡧ࡮ࡥࡩ࡯ࡨࡲࠫỰ"): bstack1ll11l1l1l_opy_(),
        bstack1l11l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡶࡺࡴ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫự"): os.environ.get(bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫỲ")),
        bstack1l11l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࡸࡥࡳࡷࡱࠫỳ"): os.environ.get(bstack1l11l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠬỴ"), False),
        bstack1l11l1l_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡡࡦࡳࡳࡺࡲࡰ࡮ࠪỵ"): bstack11lllll11l1_opy_(),
        bstack1l11l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩỶ"): bstack1111l1lll1l_opy_(),
        bstack1l11l1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡤࡦࡶࡤ࡭ࡱࡹࠧỷ"): bstack1111l1ll1l1_opy_(bstack1l1ll111l_opy_),
        bstack1l11l1l_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩỸ"): bstack1ll11l1lll_opy_(bs_config, bstack1l1ll111l_opy_.get(bstack1l11l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭ỹ"), bstack1l11l1l_opy_ (u"࠭ࠧỺ"))),
        bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩỻ"): bstack1l11l1l111_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1l11l1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡡࡺ࡮ࡲࡥࡩࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࠦࡻࡾࠤỼ").format(str(error)))
    return None
def bstack1111l1ll1l1_opy_(framework):
  return {
    bstack1l11l1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩỽ"): framework.get(bstack1l11l1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠫỾ"), bstack1l11l1l_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫỿ")),
    bstack1l11l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨἀ"): framework.get(bstack1l11l1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪἁ")),
    bstack1l11l1l_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫἂ"): framework.get(bstack1l11l1l_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ἃ")),
    bstack1l11l1l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫἄ"): bstack1l11l1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪἅ"),
    bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫἆ"): framework.get(bstack1l11l1l_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬἇ"))
  }
def bstack1ll11l1lll_opy_(bs_config, framework):
  bstack1ll1l11l11_opy_ = False
  bstack1111l1ll1_opy_ = False
  bstack1111l1lll11_opy_ = False
  if bstack1l11l1l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪἈ") in bs_config:
    bstack1111l1lll11_opy_ = True
  elif bstack1l11l1l_opy_ (u"ࠧࡢࡲࡳࠫἉ") in bs_config:
    bstack1ll1l11l11_opy_ = True
  else:
    bstack1111l1ll1_opy_ = True
  bstack11l1l1l1_opy_ = {
    bstack1l11l1l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨἊ"): bstack111ll111l_opy_.bstack1111l1l1lll_opy_(bs_config, framework),
    bstack1l11l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩἋ"): bstack1l1lll11ll_opy_.bstack1ll11l111_opy_(bs_config),
    bstack1l11l1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩἌ"): bs_config.get(bstack1l11l1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪἍ"), False),
    bstack1l11l1l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧἎ"): bstack1111l1ll1_opy_,
    bstack1l11l1l_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬἏ"): bstack1ll1l11l11_opy_,
    bstack1l11l1l_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫἐ"): bstack1111l1lll11_opy_
  }
  return bstack11l1l1l1_opy_
@bstack111l11l11l_opy_(class_method=False)
def bstack1111l1lll1l_opy_():
  try:
    bstack1111l1l1l1l_opy_ = json.loads(os.getenv(bstack1l11l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩἑ"), bstack1l11l1l_opy_ (u"ࠩࡾࢁࠬἒ")))
    return {
        bstack1l11l1l_opy_ (u"ࠪࡷࡪࡺࡴࡪࡰࡪࡷࠬἓ"): bstack1111l1l1l1l_opy_
    }
  except Exception as error:
    logger.error(bstack1l11l1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࠠࡼࡿࠥἔ").format(str(error)))
    return {}
def bstack1111lll11l1_opy_(array, bstack1111l1llll1_opy_, bstack1111l1ll111_opy_):
  result = {}
  for o in array:
    key = o[bstack1111l1llll1_opy_]
    result[key] = o[bstack1111l1ll111_opy_]
  return result
def bstack1111ll1l111_opy_(bstack1l1l1l1111_opy_=bstack1l11l1l_opy_ (u"ࠬ࠭ἕ")):
  bstack1111l1ll1ll_opy_ = bstack1l1lll11ll_opy_.on()
  bstack1111l1l1ll1_opy_ = bstack111ll111l_opy_.on()
  bstack1111l1l1l11_opy_ = percy.bstack1l1ll1l11_opy_()
  if bstack1111l1l1l11_opy_ and not bstack1111l1l1ll1_opy_ and not bstack1111l1ll1ll_opy_:
    return bstack1l1l1l1111_opy_ not in [bstack1l11l1l_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪ἖"), bstack1l11l1l_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ἗")]
  elif bstack1111l1ll1ll_opy_ and not bstack1111l1l1ll1_opy_:
    return bstack1l1l1l1111_opy_ not in [bstack1l11l1l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩἘ"), bstack1l11l1l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫἙ"), bstack1l11l1l_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧἚ")]
  return bstack1111l1ll1ll_opy_ or bstack1111l1l1ll1_opy_ or bstack1111l1l1l11_opy_
@bstack111l11l11l_opy_(class_method=False)
def bstack1111ll1l1ll_opy_(bstack1l1l1l1111_opy_, test=None):
  bstack1111l1ll11l_opy_ = bstack1l1lll11ll_opy_.on()
  if not bstack1111l1ll11l_opy_ or bstack1l1l1l1111_opy_ not in [bstack1l11l1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭Ἓ")] or test == None:
    return None
  return {
    bstack1l11l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬἜ"): bstack1111l1ll11l_opy_ and bstack111l1ll1_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬἝ"), None) == True and bstack1l1lll11ll_opy_.bstack1l1l1l1lll_opy_(test[bstack1l11l1l_opy_ (u"ࠧࡵࡣࡪࡷࠬ἞")])
  }