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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l111l11ll_opy_
bstack1llll1l1l_opy_ = Config.bstack11ll1l11l_opy_()
def bstack111l1lll111_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111l1ll11l1_opy_(bstack111l1ll1ll1_opy_, bstack111l1ll11ll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111l1ll1ll1_opy_):
        with open(bstack111l1ll1ll1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111l1lll111_opy_(bstack111l1ll1ll1_opy_):
        pac = get_pac(url=bstack111l1ll1ll1_opy_)
    else:
        raise Exception(bstack1l11l1l_opy_ (u"ࠬࡖࡡࡤࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠬᴁ").format(bstack111l1ll1ll1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l11l1l_opy_ (u"ࠨ࠸࠯࠺࠱࠼࠳࠾ࠢᴂ"), 80))
        bstack111l1ll1l1l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111l1ll1l1l_opy_ = bstack1l11l1l_opy_ (u"ࠧ࠱࠰࠳࠲࠵࠴࠰ࠨᴃ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111l1ll11ll_opy_, bstack111l1ll1l1l_opy_)
    return proxy_url
def bstack1lll1111ll_opy_(config):
    return bstack1l11l1l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᴄ") in config or bstack1l11l1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᴅ") in config
def bstack1ll1l111l1_opy_(config):
    if not bstack1lll1111ll_opy_(config):
        return
    if config.get(bstack1l11l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᴆ")):
        return config.get(bstack1l11l1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᴇ"))
    if config.get(bstack1l11l1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᴈ")):
        return config.get(bstack1l11l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᴉ"))
def bstack1lll1lll_opy_(config, bstack111l1ll11ll_opy_):
    proxy = bstack1ll1l111l1_opy_(config)
    proxies = {}
    if config.get(bstack1l11l1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᴊ")) or config.get(bstack1l11l1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᴋ")):
        if proxy.endswith(bstack1l11l1l_opy_ (u"ࠩ࠱ࡴࡦࡩࠧᴌ")):
            proxies = bstack1111ll1ll_opy_(proxy, bstack111l1ll11ll_opy_)
        else:
            proxies = {
                bstack1l11l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᴍ"): proxy
            }
    bstack1llll1l1l_opy_.bstack11l1llll_opy_(bstack1l11l1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫᴎ"), proxies)
    return proxies
def bstack1111ll1ll_opy_(bstack111l1ll1ll1_opy_, bstack111l1ll11ll_opy_):
    proxies = {}
    global bstack111l1ll1lll_opy_
    if bstack1l11l1l_opy_ (u"ࠬࡖࡁࡄࡡࡓࡖࡔ࡞࡙ࠨᴏ") in globals():
        return bstack111l1ll1lll_opy_
    try:
        proxy = bstack111l1ll11l1_opy_(bstack111l1ll1ll1_opy_, bstack111l1ll11ll_opy_)
        if bstack1l11l1l_opy_ (u"ࠨࡄࡊࡔࡈࡇ࡙ࠨᴐ") in proxy:
            proxies = {}
        elif bstack1l11l1l_opy_ (u"ࠢࡉࡖࡗࡔࠧᴑ") in proxy or bstack1l11l1l_opy_ (u"ࠣࡊࡗࡘࡕ࡙ࠢᴒ") in proxy or bstack1l11l1l_opy_ (u"ࠤࡖࡓࡈࡑࡓࠣᴓ") in proxy:
            bstack111l1ll1l11_opy_ = proxy.split(bstack1l11l1l_opy_ (u"ࠥࠤࠧᴔ"))
            if bstack1l11l1l_opy_ (u"ࠦ࠿࠵࠯ࠣᴕ") in bstack1l11l1l_opy_ (u"ࠧࠨᴖ").join(bstack111l1ll1l11_opy_[1:]):
                proxies = {
                    bstack1l11l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᴗ"): bstack1l11l1l_opy_ (u"ࠢࠣᴘ").join(bstack111l1ll1l11_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l11l1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᴙ"): str(bstack111l1ll1l11_opy_[0]).lower() + bstack1l11l1l_opy_ (u"ࠤ࠽࠳࠴ࠨᴚ") + bstack1l11l1l_opy_ (u"ࠥࠦᴛ").join(bstack111l1ll1l11_opy_[1:])
                }
        elif bstack1l11l1l_opy_ (u"ࠦࡕࡘࡏ࡙࡛ࠥᴜ") in proxy:
            bstack111l1ll1l11_opy_ = proxy.split(bstack1l11l1l_opy_ (u"ࠧࠦࠢᴝ"))
            if bstack1l11l1l_opy_ (u"ࠨ࠺࠰࠱ࠥᴞ") in bstack1l11l1l_opy_ (u"ࠢࠣᴟ").join(bstack111l1ll1l11_opy_[1:]):
                proxies = {
                    bstack1l11l1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᴠ"): bstack1l11l1l_opy_ (u"ࠤࠥᴡ").join(bstack111l1ll1l11_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l11l1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᴢ"): bstack1l11l1l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᴣ") + bstack1l11l1l_opy_ (u"ࠧࠨᴤ").join(bstack111l1ll1l11_opy_[1:])
                }
        else:
            proxies = {
                bstack1l11l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᴥ"): proxy
            }
    except Exception as e:
        print(bstack1l11l1l_opy_ (u"ࠢࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦᴦ"), bstack11l111l11ll_opy_.format(bstack111l1ll1ll1_opy_, str(e)))
    bstack111l1ll1lll_opy_ = proxies
    return proxies