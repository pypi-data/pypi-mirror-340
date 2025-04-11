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
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack11llllll11l_opy_ as bstack11llll1lll1_opy_, EVENTS
from bstack_utils.bstack1l1llll1l_opy_ import bstack1l1llll1l_opy_
from bstack_utils.helper import bstack1l1ll1l1l_opy_, bstack111ll1ll11_opy_, bstack1l11l1l111_opy_, bstack11llll1l1ll_opy_, \
  bstack11llll1ll1l_opy_, bstack1ll11l1l1l_opy_, get_host_info, bstack11lllll11l1_opy_, bstack1ll1lllll1_opy_, bstack111l11l11l_opy_, bstack111l1ll1_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1l111l1ll_opy_ import get_logger
from bstack_utils.bstack1111l11l_opy_ import bstack1lllll11l1l_opy_
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack1111l11l_opy_ = bstack1lllll11l1l_opy_()
@bstack111l11l11l_opy_(class_method=False)
def _11llll1l1l1_opy_(driver, bstack111l111l11_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1l11l1l_opy_ (u"ࠧࡰࡵࡢࡲࡦࡳࡥࠨᕍ"): caps.get(bstack1l11l1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᕎ"), None),
        bstack1l11l1l_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᕏ"): bstack111l111l11_opy_.get(bstack1l11l1l_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᕐ"), None),
        bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪᕑ"): caps.get(bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᕒ"), None),
        bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᕓ"): caps.get(bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᕔ"), None)
    }
  except Exception as error:
    logger.debug(bstack1l11l1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬᕕ") + str(error))
  return response
def on():
    if os.environ.get(bstack1l11l1l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᕖ"), None) is None or os.environ[bstack1l11l1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᕗ")] == bstack1l11l1l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᕘ"):
        return False
    return True
def bstack1ll11l111_opy_(config):
  return config.get(bstack1l11l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᕙ"), False) or any([p.get(bstack1l11l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᕚ"), False) == True for p in config.get(bstack1l11l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᕛ"), [])])
def bstack1llll1l111_opy_(config, bstack11l1l11l1_opy_):
  try:
    if not bstack1l11l1l111_opy_(config):
      return False
    bstack11lllll11ll_opy_ = config.get(bstack1l11l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᕜ"), False)
    if int(bstack11l1l11l1_opy_) < len(config.get(bstack1l11l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᕝ"), [])) and config[bstack1l11l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᕞ")][bstack11l1l11l1_opy_]:
      bstack11lll1ll1ll_opy_ = config[bstack1l11l1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᕟ")][bstack11l1l11l1_opy_].get(bstack1l11l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᕠ"), None)
    else:
      bstack11lll1ll1ll_opy_ = config.get(bstack1l11l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᕡ"), None)
    if bstack11lll1ll1ll_opy_ != None:
      bstack11lllll11ll_opy_ = bstack11lll1ll1ll_opy_
    bstack11llllll1ll_opy_ = os.getenv(bstack1l11l1l_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᕢ")) is not None and len(os.getenv(bstack1l11l1l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᕣ"))) > 0 and os.getenv(bstack1l11l1l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᕤ")) != bstack1l11l1l_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᕥ")
    return bstack11lllll11ll_opy_ and bstack11llllll1ll_opy_
  except Exception as error:
    logger.debug(bstack1l11l1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡪࡸࡩࡧࡻ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫᕦ") + str(error))
  return False
def bstack1l1l1l1lll_opy_(test_tags):
  bstack1ll1ll1l1ll_opy_ = os.getenv(bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᕧ"))
  if bstack1ll1ll1l1ll_opy_ is None:
    return True
  bstack1ll1ll1l1ll_opy_ = json.loads(bstack1ll1ll1l1ll_opy_)
  try:
    include_tags = bstack1ll1ll1l1ll_opy_[bstack1l11l1l_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᕨ")] if bstack1l11l1l_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᕩ") in bstack1ll1ll1l1ll_opy_ and isinstance(bstack1ll1ll1l1ll_opy_[bstack1l11l1l_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᕪ")], list) else []
    exclude_tags = bstack1ll1ll1l1ll_opy_[bstack1l11l1l_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᕫ")] if bstack1l11l1l_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᕬ") in bstack1ll1ll1l1ll_opy_ and isinstance(bstack1ll1ll1l1ll_opy_[bstack1l11l1l_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᕭ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1l11l1l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡺࡦࡲࡩࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡤࡲࡳ࡯࡮ࡨ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠤࠧᕮ") + str(error))
  return False
def bstack11lll1lll1l_opy_(config, bstack11llll11l1l_opy_, bstack11llll1l11l_opy_, bstack11llll1llll_opy_):
  bstack11llll1ll11_opy_ = bstack11llll1l1ll_opy_(config)
  bstack11lllll1l11_opy_ = bstack11llll1ll1l_opy_(config)
  if bstack11llll1ll11_opy_ is None or bstack11lllll1l11_opy_ is None:
    logger.error(bstack1l11l1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧᕯ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1l11l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᕰ"), bstack1l11l1l_opy_ (u"ࠨࡽࢀࠫᕱ")))
    data = {
        bstack1l11l1l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᕲ"): config[bstack1l11l1l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᕳ")],
        bstack1l11l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᕴ"): config.get(bstack1l11l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᕵ"), os.path.basename(os.getcwd())),
        bstack1l11l1l_opy_ (u"࠭ࡳࡵࡣࡵࡸ࡙࡯࡭ࡦࠩᕶ"): bstack1l1ll1l1l_opy_(),
        bstack1l11l1l_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᕷ"): config.get(bstack1l11l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᕸ"), bstack1l11l1l_opy_ (u"ࠩࠪᕹ")),
        bstack1l11l1l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪᕺ"): {
            bstack1l11l1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫᕻ"): bstack11llll11l1l_opy_,
            bstack1l11l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᕼ"): bstack11llll1l11l_opy_,
            bstack1l11l1l_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᕽ"): __version__,
            bstack1l11l1l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩᕾ"): bstack1l11l1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᕿ"),
            bstack1l11l1l_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᖀ"): bstack1l11l1l_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬᖁ"),
            bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᖂ"): bstack11llll1llll_opy_
        },
        bstack1l11l1l_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧᖃ"): settings,
        bstack1l11l1l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࡃࡰࡰࡷࡶࡴࡲࠧᖄ"): bstack11lllll11l1_opy_(),
        bstack1l11l1l_opy_ (u"ࠧࡤ࡫ࡌࡲ࡫ࡵࠧᖅ"): bstack1ll11l1l1l_opy_(),
        bstack1l11l1l_opy_ (u"ࠨࡪࡲࡷࡹࡏ࡮ࡧࡱࠪᖆ"): get_host_info(),
        bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᖇ"): bstack1l11l1l111_opy_(config)
    }
    headers = {
        bstack1l11l1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᖈ"): bstack1l11l1l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧᖉ"),
    }
    config = {
        bstack1l11l1l_opy_ (u"ࠬࡧࡵࡵࡪࠪᖊ"): (bstack11llll1ll11_opy_, bstack11lllll1l11_opy_),
        bstack1l11l1l_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᖋ"): headers
    }
    response = bstack1ll1lllll1_opy_(bstack1l11l1l_opy_ (u"ࠧࡑࡑࡖࡘࠬᖌ"), bstack11llll1lll1_opy_ + bstack1l11l1l_opy_ (u"ࠨ࠱ࡹ࠶࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳࠨᖍ"), data, config)
    bstack11llll111ll_opy_ = response.json()
    if bstack11llll111ll_opy_[bstack1l11l1l_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᖎ")]:
      parsed = json.loads(os.getenv(bstack1l11l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᖏ"), bstack1l11l1l_opy_ (u"ࠫࢀࢃࠧᖐ")))
      parsed[bstack1l11l1l_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᖑ")] = bstack11llll111ll_opy_[bstack1l11l1l_opy_ (u"࠭ࡤࡢࡶࡤࠫᖒ")][bstack1l11l1l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᖓ")]
      os.environ[bstack1l11l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᖔ")] = json.dumps(parsed)
      bstack1l1llll1l_opy_.bstack11ll1l1l1_opy_(bstack11llll111ll_opy_[bstack1l11l1l_opy_ (u"ࠩࡧࡥࡹࡧࠧᖕ")][bstack1l11l1l_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᖖ")])
      bstack1l1llll1l_opy_.bstack11lllll1l1l_opy_(bstack11llll111ll_opy_[bstack1l11l1l_opy_ (u"ࠫࡩࡧࡴࡢࠩᖗ")][bstack1l11l1l_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᖘ")])
      bstack1l1llll1l_opy_.store()
      return bstack11llll111ll_opy_[bstack1l11l1l_opy_ (u"࠭ࡤࡢࡶࡤࠫᖙ")][bstack1l11l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬᖚ")], bstack11llll111ll_opy_[bstack1l11l1l_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᖛ")][bstack1l11l1l_opy_ (u"ࠩ࡬ࡨࠬᖜ")]
    else:
      logger.error(bstack1l11l1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࠫᖝ") + bstack11llll111ll_opy_[bstack1l11l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᖞ")])
      if bstack11llll111ll_opy_[bstack1l11l1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᖟ")] == bstack1l11l1l_opy_ (u"࠭ࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡱࡣࡶࡷࡪࡪ࠮ࠨᖠ"):
        for bstack11llll1111l_opy_ in bstack11llll111ll_opy_[bstack1l11l1l_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧᖡ")]:
          logger.error(bstack11llll1111l_opy_[bstack1l11l1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᖢ")])
      return None, None
  except Exception as error:
    logger.error(bstack1l11l1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡷࡻ࡮ࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠥᖣ") +  str(error))
    return None, None
def bstack11lllll1ll1_opy_():
  if os.getenv(bstack1l11l1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᖤ")) is None:
    return {
        bstack1l11l1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᖥ"): bstack1l11l1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᖦ"),
        bstack1l11l1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᖧ"): bstack1l11l1l_opy_ (u"ࠧࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡪࡤࡨࠥ࡬ࡡࡪ࡮ࡨࡨ࠳࠭ᖨ")
    }
  data = {bstack1l11l1l_opy_ (u"ࠨࡧࡱࡨ࡙࡯࡭ࡦࠩᖩ"): bstack1l1ll1l1l_opy_()}
  headers = {
      bstack1l11l1l_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩᖪ"): bstack1l11l1l_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࠫᖫ") + os.getenv(bstack1l11l1l_opy_ (u"ࠦࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠤᖬ")),
      bstack1l11l1l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᖭ"): bstack1l11l1l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᖮ")
  }
  response = bstack1ll1lllll1_opy_(bstack1l11l1l_opy_ (u"ࠧࡑࡗࡗࠫᖯ"), bstack11llll1lll1_opy_ + bstack1l11l1l_opy_ (u"ࠨ࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷ࠴ࡹࡴࡰࡲࠪᖰ"), data, { bstack1l11l1l_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᖱ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1l11l1l_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡔࡦࡵࡷࠤࡗࡻ࡮ࠡ࡯ࡤࡶࡰ࡫ࡤࠡࡣࡶࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠠࡢࡶࠣࠦᖲ") + bstack111ll1ll11_opy_().isoformat() + bstack1l11l1l_opy_ (u"ࠫ࡟࠭ᖳ"))
      return {bstack1l11l1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᖴ"): bstack1l11l1l_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᖵ"), bstack1l11l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᖶ"): bstack1l11l1l_opy_ (u"ࠨࠩᖷ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1l11l1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡯࡯࡯ࠢࡲࡪࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰ࠽ࠤࠧᖸ") + str(error))
    return {
        bstack1l11l1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᖹ"): bstack1l11l1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᖺ"),
        bstack1l11l1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᖻ"): str(error)
    }
def bstack11lll1lll11_opy_(bstack11llll11111_opy_):
    return re.match(bstack1l11l1l_opy_ (u"ࡸࠧ࡟࡞ࡧ࠯࠭ࡢ࠮࡝ࡦ࠮࠭ࡄࠪࠧᖼ"), bstack11llll11111_opy_.strip()) is not None
def bstack11llllll_opy_(caps, options, desired_capabilities={}):
    try:
        if options:
          bstack11lllll1lll_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11lllll1lll_opy_ = desired_capabilities
        else:
          bstack11lllll1lll_opy_ = {}
        bstack11llllll111_opy_ = (bstack11lllll1lll_opy_.get(bstack1l11l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᖽ"), bstack1l11l1l_opy_ (u"ࠨࠩᖾ")).lower() or caps.get(bstack1l11l1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᖿ"), bstack1l11l1l_opy_ (u"ࠪࠫᗀ")).lower())
        if bstack11llllll111_opy_ == bstack1l11l1l_opy_ (u"ࠫ࡮ࡵࡳࠨᗁ"):
            return True
        if bstack11llllll111_opy_ == bstack1l11l1l_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࠭ᗂ"):
            bstack11llll11lll_opy_ = str(float(caps.get(bstack1l11l1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᗃ")) or bstack11lllll1lll_opy_.get(bstack1l11l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᗄ"), {}).get(bstack1l11l1l_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᗅ"),bstack1l11l1l_opy_ (u"ࠩࠪᗆ"))))
            if bstack11llllll111_opy_ == bstack1l11l1l_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࠫᗇ") and int(bstack11llll11lll_opy_.split(bstack1l11l1l_opy_ (u"ࠫ࠳࠭ᗈ"))[0]) < float(bstack11llll11l11_opy_):
                logger.warning(str(bstack11lll1llll1_opy_))
                return False
            return True
        bstack1ll1ll11111_opy_ = caps.get(bstack1l11l1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᗉ"), {}).get(bstack1l11l1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᗊ"), caps.get(bstack1l11l1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧᗋ"), bstack1l11l1l_opy_ (u"ࠨࠩᗌ")))
        if bstack1ll1ll11111_opy_:
            logger.warn(bstack1l11l1l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᗍ"))
            return False
        browser = caps.get(bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᗎ"), bstack1l11l1l_opy_ (u"ࠫࠬᗏ")).lower() or bstack11lllll1lll_opy_.get(bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᗐ"), bstack1l11l1l_opy_ (u"࠭ࠧᗑ")).lower()
        if browser != bstack1l11l1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᗒ"):
            logger.warning(bstack1l11l1l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᗓ"))
            return False
        browser_version = caps.get(bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᗔ")) or caps.get(bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᗕ")) or bstack11lllll1lll_opy_.get(bstack1l11l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᗖ")) or bstack11lllll1lll_opy_.get(bstack1l11l1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᗗ"), {}).get(bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᗘ")) or bstack11lllll1lll_opy_.get(bstack1l11l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᗙ"), {}).get(bstack1l11l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᗚ"))
        if browser_version and browser_version != bstack1l11l1l_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩᗛ") and int(browser_version.split(bstack1l11l1l_opy_ (u"ࠪ࠲ࠬᗜ"))[0]) <= 98:
            logger.warning(bstack1l11l1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡧࡳࡧࡤࡸࡪࡸࠠࡵࡪࡤࡲࠥ࠿࠸࠯ࠤᗝ"))
            return False
        if not options:
            bstack1ll1lll1111_opy_ = caps.get(bstack1l11l1l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᗞ")) or bstack11lllll1lll_opy_.get(bstack1l11l1l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᗟ"), {})
            if bstack1l11l1l_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫᗠ") in bstack1ll1lll1111_opy_.get(bstack1l11l1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᗡ"), []):
                logger.warn(bstack1l11l1l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦᗢ"))
                return False
        return True
    except Exception as error:
        logger.debug(bstack1l11l1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡥࡱ࡯ࡤࡢࡶࡨࠤࡦ࠷࠱ࡺࠢࡶࡹࡵࡶ࡯ࡳࡶࠣ࠾ࠧᗣ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1llll11ll1l_opy_ = config.get(bstack1l11l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᗤ"), {})
    bstack1llll11ll1l_opy_[bstack1l11l1l_opy_ (u"ࠬࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨᗥ")] = os.getenv(bstack1l11l1l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᗦ"))
    bstack11llll1l111_opy_ = json.loads(os.getenv(bstack1l11l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᗧ"), bstack1l11l1l_opy_ (u"ࠨࡽࢀࠫᗨ"))).get(bstack1l11l1l_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᗩ"))
    caps[bstack1l11l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᗪ")] = True
    if not config[bstack1l11l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ᗫ")].get(bstack1l11l1l_opy_ (u"ࠧࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠦᗬ")):
      if bstack1l11l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᗭ") in caps:
        caps[bstack1l11l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᗮ")][bstack1l11l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᗯ")] = bstack1llll11ll1l_opy_
        caps[bstack1l11l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᗰ")][bstack1l11l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᗱ")][bstack1l11l1l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᗲ")] = bstack11llll1l111_opy_
      else:
        caps[bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᗳ")] = bstack1llll11ll1l_opy_
        caps[bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᗴ")][bstack1l11l1l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᗵ")] = bstack11llll1l111_opy_
  except Exception as error:
    logger.debug(bstack1l11l1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠮ࠡࡇࡵࡶࡴࡸ࠺ࠡࠤᗶ") +  str(error))
def bstack1111llll_opy_(driver, bstack11llll111l1_opy_):
  try:
    setattr(driver, bstack1l11l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩᗷ"), True)
    session = driver.session_id
    if session:
      bstack11lll1lllll_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11lll1lllll_opy_ = False
      bstack11lll1lllll_opy_ = url.scheme in [bstack1l11l1l_opy_ (u"ࠥ࡬ࡹࡺࡰࠣᗸ"), bstack1l11l1l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥᗹ")]
      if bstack11lll1lllll_opy_:
        if bstack11llll111l1_opy_:
          logger.info(bstack1l11l1l_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡫ࡵࡲࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡫ࡥࡸࠦࡳࡵࡣࡵࡸࡪࡪ࠮ࠡࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡣࡧࡪ࡭ࡳࠦ࡭ࡰ࡯ࡨࡲࡹࡧࡲࡪ࡮ࡼ࠲ࠧᗺ"))
      return bstack11llll111l1_opy_
  except Exception as e:
    logger.error(bstack1l11l1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤᗻ") + str(e))
    return False
def bstack11ll1lll11_opy_(driver, name, path):
  try:
    bstack1ll1l1111ll_opy_ = {
        bstack1l11l1l_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠧᗼ"): threading.current_thread().current_test_uuid,
        bstack1l11l1l_opy_ (u"ࠨࡶ࡫ࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ᗽ"): os.environ.get(bstack1l11l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᗾ"), bstack1l11l1l_opy_ (u"ࠪࠫᗿ")),
        bstack1l11l1l_opy_ (u"ࠫࡹ࡮ࡊࡸࡶࡗࡳࡰ࡫࡮ࠨᘀ"): os.environ.get(bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᘁ"), bstack1l11l1l_opy_ (u"࠭ࠧᘂ"))
    }
    bstack1ll1ll1ll1l_opy_ = bstack1111l11l_opy_.bstack1ll11llll11_opy_(EVENTS.bstack1lll1l11ll_opy_.value)
    logger.debug(bstack1l11l1l_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡥࡻ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪᘃ"))
    try:
      if (bstack111l1ll1_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨᘄ"), None) and bstack111l1ll1_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᘅ"), None)):
        scripts = {bstack1l11l1l_opy_ (u"ࠪࡷࡨࡧ࡮ࠨᘆ"): bstack1l1llll1l_opy_.perform_scan}
        bstack11llll11ll1_opy_ = json.loads(scripts[bstack1l11l1l_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᘇ")].replace(bstack1l11l1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣᘈ"), bstack1l11l1l_opy_ (u"ࠨࠢᘉ")))
        bstack11llll11ll1_opy_[bstack1l11l1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᘊ")][bstack1l11l1l_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨᘋ")] = None
        scripts[bstack1l11l1l_opy_ (u"ࠤࡶࡧࡦࡴࠢᘌ")] = bstack1l11l1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᘍ") + json.dumps(bstack11llll11ll1_opy_)
        bstack1l1llll1l_opy_.bstack11ll1l1l1_opy_(scripts)
        bstack1l1llll1l_opy_.store()
        logger.debug(driver.execute_script(bstack1l1llll1l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l1llll1l_opy_.perform_scan, {bstack1l11l1l_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦᘎ"): name}))
      bstack1111l11l_opy_.end(EVENTS.bstack1lll1l11ll_opy_.value, bstack1ll1ll1ll1l_opy_ + bstack1l11l1l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᘏ"), bstack1ll1ll1ll1l_opy_ + bstack1l11l1l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᘐ"), True, None)
    except Exception as error:
      bstack1111l11l_opy_.end(EVENTS.bstack1lll1l11ll_opy_.value, bstack1ll1ll1ll1l_opy_ + bstack1l11l1l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᘑ"), bstack1ll1ll1ll1l_opy_ + bstack1l11l1l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᘒ"), False, str(error))
    bstack1ll1ll1ll1l_opy_ = bstack1111l11l_opy_.bstack11lllll1111_opy_(EVENTS.bstack1ll1l1lll1l_opy_.value)
    bstack1111l11l_opy_.mark(bstack1ll1ll1ll1l_opy_ + bstack1l11l1l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᘓ"))
    try:
      if (bstack111l1ll1_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪᘔ"), None) and bstack111l1ll1_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᘕ"), None)):
        scripts = {bstack1l11l1l_opy_ (u"ࠬࡹࡣࡢࡰࠪᘖ"): bstack1l1llll1l_opy_.perform_scan}
        bstack11llll11ll1_opy_ = json.loads(scripts[bstack1l11l1l_opy_ (u"ࠨࡳࡤࡣࡱࠦᘗ")].replace(bstack1l11l1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥᘘ"), bstack1l11l1l_opy_ (u"ࠣࠤᘙ")))
        bstack11llll11ll1_opy_[bstack1l11l1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᘚ")][bstack1l11l1l_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪᘛ")] = None
        scripts[bstack1l11l1l_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᘜ")] = bstack1l11l1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣᘝ") + json.dumps(bstack11llll11ll1_opy_)
        bstack1l1llll1l_opy_.bstack11ll1l1l1_opy_(scripts)
        bstack1l1llll1l_opy_.store()
        logger.debug(driver.execute_script(bstack1l1llll1l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l1llll1l_opy_.bstack11lllll111l_opy_, bstack1ll1l1111ll_opy_))
      bstack1111l11l_opy_.end(bstack1ll1ll1ll1l_opy_, bstack1ll1ll1ll1l_opy_ + bstack1l11l1l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᘞ"), bstack1ll1ll1ll1l_opy_ + bstack1l11l1l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᘟ"),True, None)
    except Exception as error:
      bstack1111l11l_opy_.end(bstack1ll1ll1ll1l_opy_, bstack1ll1ll1ll1l_opy_ + bstack1l11l1l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᘠ"), bstack1ll1ll1ll1l_opy_ + bstack1l11l1l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᘡ"),False, str(error))
    logger.info(bstack1l11l1l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨᘢ"))
  except Exception as bstack1ll1ll1llll_opy_:
    logger.error(bstack1l11l1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨᘣ") + str(path) + bstack1l11l1l_opy_ (u"ࠧࠦࡅࡳࡴࡲࡶࠥࡀࠢᘤ") + str(bstack1ll1ll1llll_opy_))
def bstack11llllll1l1_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1l11l1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧᘥ")) and str(caps.get(bstack1l11l1l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨᘦ"))).lower() == bstack1l11l1l_opy_ (u"ࠣࡣࡱࡨࡷࡵࡩࡥࠤᘧ"):
        bstack11llll11lll_opy_ = caps.get(bstack1l11l1l_opy_ (u"ࠤࡤࡴࡵ࡯ࡵ࡮࠼ࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦᘨ")) or caps.get(bstack1l11l1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᘩ"))
        if bstack11llll11lll_opy_ and int(str(bstack11llll11lll_opy_)) < bstack11llll11l11_opy_:
            return False
    return True