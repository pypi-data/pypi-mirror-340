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
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11ll11111l1_opy_, bstack1llll1l1l1_opy_, bstack111l1ll1_opy_, bstack1l11ll1lll_opy_, \
    bstack11l11llll1l_opy_
from bstack_utils.measure import measure
def bstack11ll1l1l_opy_(bstack111l111llll_opy_):
    for driver in bstack111l111llll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l11111l1_opy_, stage=STAGE.bstack1l11l111ll_opy_)
def bstack1l1ll11l1l_opy_(driver, status, reason=bstack1l11l1l_opy_ (u"࠭ࠧᵲ")):
    bstack1llll1l1l_opy_ = Config.bstack11ll1l11l_opy_()
    if bstack1llll1l1l_opy_.bstack111l11l111_opy_():
        return
    bstack111l11lll_opy_ = bstack1111l111l_opy_(bstack1l11l1l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᵳ"), bstack1l11l1l_opy_ (u"ࠨࠩᵴ"), status, reason, bstack1l11l1l_opy_ (u"ࠩࠪᵵ"), bstack1l11l1l_opy_ (u"ࠪࠫᵶ"))
    driver.execute_script(bstack111l11lll_opy_)
@measure(event_name=EVENTS.bstack1l11111l1_opy_, stage=STAGE.bstack1l11l111ll_opy_)
def bstack11l1lll111_opy_(page, status, reason=bstack1l11l1l_opy_ (u"ࠫࠬᵷ")):
    try:
        if page is None:
            return
        bstack1llll1l1l_opy_ = Config.bstack11ll1l11l_opy_()
        if bstack1llll1l1l_opy_.bstack111l11l111_opy_():
            return
        bstack111l11lll_opy_ = bstack1111l111l_opy_(bstack1l11l1l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨᵸ"), bstack1l11l1l_opy_ (u"࠭ࠧᵹ"), status, reason, bstack1l11l1l_opy_ (u"ࠧࠨᵺ"), bstack1l11l1l_opy_ (u"ࠨࠩᵻ"))
        page.evaluate(bstack1l11l1l_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥᵼ"), bstack111l11lll_opy_)
    except Exception as e:
        print(bstack1l11l1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࢁࡽࠣᵽ"), e)
def bstack1111l111l_opy_(type, name, status, reason, bstack11ll1ll1l1_opy_, bstack1ll11l11_opy_):
    bstack1l1l11l1ll_opy_ = {
        bstack1l11l1l_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫᵾ"): type,
        bstack1l11l1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᵿ"): {}
    }
    if type == bstack1l11l1l_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨᶀ"):
        bstack1l1l11l1ll_opy_[bstack1l11l1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᶁ")][bstack1l11l1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᶂ")] = bstack11ll1ll1l1_opy_
        bstack1l1l11l1ll_opy_[bstack1l11l1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᶃ")][bstack1l11l1l_opy_ (u"ࠪࡨࡦࡺࡡࠨᶄ")] = json.dumps(str(bstack1ll11l11_opy_))
    if type == bstack1l11l1l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᶅ"):
        bstack1l1l11l1ll_opy_[bstack1l11l1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᶆ")][bstack1l11l1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᶇ")] = name
    if type == bstack1l11l1l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᶈ"):
        bstack1l1l11l1ll_opy_[bstack1l11l1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᶉ")][bstack1l11l1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᶊ")] = status
        if status == bstack1l11l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᶋ") and str(reason) != bstack1l11l1l_opy_ (u"ࠦࠧᶌ"):
            bstack1l1l11l1ll_opy_[bstack1l11l1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᶍ")][bstack1l11l1l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ᶎ")] = json.dumps(str(reason))
    bstack111l1l1ll_opy_ = bstack1l11l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬᶏ").format(json.dumps(bstack1l1l11l1ll_opy_))
    return bstack111l1l1ll_opy_
def bstack1ll1l11lll_opy_(url, config, logger, bstack11ll1ll11_opy_=False):
    hostname = bstack1llll1l1l1_opy_(url)
    is_private = bstack1l11ll1lll_opy_(hostname)
    try:
        if is_private or bstack11ll1ll11_opy_:
            file_path = bstack11ll11111l1_opy_(bstack1l11l1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᶐ"), bstack1l11l1l_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨᶑ"), logger)
            if os.environ.get(bstack1l11l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᶒ")) and eval(
                    os.environ.get(bstack1l11l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᶓ"))):
                return
            if (bstack1l11l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᶔ") in config and not config[bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᶕ")]):
                os.environ[bstack1l11l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᶖ")] = str(True)
                bstack111l111lll1_opy_ = {bstack1l11l1l_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪᶗ"): hostname}
                bstack11l11llll1l_opy_(bstack1l11l1l_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨᶘ"), bstack1l11l1l_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨᶙ"), bstack111l111lll1_opy_, logger)
    except Exception as e:
        pass
def bstack1l11lll1_opy_(caps, bstack111l111ll1l_opy_):
    if bstack1l11l1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᶚ") in caps:
        caps[bstack1l11l1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᶛ")][bstack1l11l1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬᶜ")] = True
        if bstack111l111ll1l_opy_:
            caps[bstack1l11l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᶝ")][bstack1l11l1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᶞ")] = bstack111l111ll1l_opy_
    else:
        caps[bstack1l11l1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧᶟ")] = True
        if bstack111l111ll1l_opy_:
            caps[bstack1l11l1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᶠ")] = bstack111l111ll1l_opy_
def bstack111l1l1l11l_opy_(bstack111l11lll1_opy_):
    bstack111l111ll11_opy_ = bstack111l1ll1_opy_(threading.current_thread(), bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨᶡ"), bstack1l11l1l_opy_ (u"ࠬ࠭ᶢ"))
    if bstack111l111ll11_opy_ == bstack1l11l1l_opy_ (u"࠭ࠧᶣ") or bstack111l111ll11_opy_ == bstack1l11l1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᶤ"):
        threading.current_thread().testStatus = bstack111l11lll1_opy_
    else:
        if bstack111l11lll1_opy_ == bstack1l11l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᶥ"):
            threading.current_thread().testStatus = bstack111l11lll1_opy_