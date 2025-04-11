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
import logging
import bstack_utils.accessibility as bstack1l1lll11ll_opy_
from bstack_utils.helper import bstack111l1ll1_opy_
logger = logging.getLogger(__name__)
def bstack1l1lll11l1_opy_(bstack1l1lll11_opy_):
  return True if bstack1l1lll11_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1l1llll111_opy_(context, *args):
    tags = getattr(args[0], bstack1l11l1l_opy_ (u"ࠬࡺࡡࡨࡵࠪᙎ"), [])
    bstack11ll11111l_opy_ = bstack1l1lll11ll_opy_.bstack1l1l1l1lll_opy_(tags)
    threading.current_thread().isA11yTest = bstack11ll11111l_opy_
    try:
      bstack11l1ll1l_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1lll11l1_opy_(bstack1l11l1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬᙏ")) else context.browser
      if bstack11l1ll1l_opy_ and bstack11l1ll1l_opy_.session_id and bstack11ll11111l_opy_ and bstack111l1ll1_opy_(
              threading.current_thread(), bstack1l11l1l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᙐ"), None):
          threading.current_thread().isA11yTest = bstack1l1lll11ll_opy_.bstack1111llll_opy_(bstack11l1ll1l_opy_, bstack11ll11111l_opy_)
    except Exception as e:
       logger.debug(bstack1l11l1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡥ࠶࠷ࡹࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨᙑ").format(str(e)))
def bstack1l1111lll_opy_(bstack11l1ll1l_opy_):
    if bstack111l1ll1_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᙒ"), None) and bstack111l1ll1_opy_(
      threading.current_thread(), bstack1l11l1l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᙓ"), None) and not bstack111l1ll1_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠫࡦ࠷࠱ࡺࡡࡶࡸࡴࡶࠧᙔ"), False):
      threading.current_thread().a11y_stop = True
      bstack1l1lll11ll_opy_.bstack11ll1lll11_opy_(bstack11l1ll1l_opy_, name=bstack1l11l1l_opy_ (u"ࠧࠨᙕ"), path=bstack1l11l1l_opy_ (u"ࠨࠢᙖ"))