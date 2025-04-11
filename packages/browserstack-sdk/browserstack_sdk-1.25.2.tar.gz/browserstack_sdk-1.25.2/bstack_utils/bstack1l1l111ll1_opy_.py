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
from browserstack_sdk.bstack1l1l11l1l1_opy_ import bstack1lll1l111l_opy_
from browserstack_sdk.bstack111lll1l1l_opy_ import RobotHandler
def bstack1llll1ll11_opy_(framework):
    if framework.lower() == bstack1l11l1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᦏ"):
        return bstack1lll1l111l_opy_.version()
    elif framework.lower() == bstack1l11l1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬᦐ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l11l1l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧᦑ"):
        import behave
        return behave.__version__
    else:
        return bstack1l11l1l_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩᦒ")
def bstack1ll1l11l1l_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1l11l1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᦓ"))
        framework_version.append(importlib.metadata.version(bstack1l11l1l_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧᦔ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1l11l1l_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᦕ"))
        framework_version.append(importlib.metadata.version(bstack1l11l1l_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᦖ")))
    except:
        pass
    return {
        bstack1l11l1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᦗ"): bstack1l11l1l_opy_ (u"ࠧࡠࠩᦘ").join(framework_name),
        bstack1l11l1l_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩᦙ"): bstack1l11l1l_opy_ (u"ࠩࡢࠫᦚ").join(framework_version)
    }