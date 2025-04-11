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
from uuid import uuid4
from bstack_utils.helper import bstack1l1ll1l1l_opy_, bstack11l1l111111_opy_
from bstack_utils.bstack1l1l1l11l1_opy_ import bstack111l1l1l111_opy_
class bstack111llll111_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack111l1111ll1_opy_=None, bstack111l111l1l1_opy_=True, bstack1l11ll1llll_opy_=None, bstack1l1l1l1111_opy_=None, result=None, duration=None, bstack111lll11ll_opy_=None, meta={}):
        self.bstack111lll11ll_opy_ = bstack111lll11ll_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack111l111l1l1_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack111l1111ll1_opy_ = bstack111l1111ll1_opy_
        self.bstack1l11ll1llll_opy_ = bstack1l11ll1llll_opy_
        self.bstack1l1l1l1111_opy_ = bstack1l1l1l1111_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111l1l11ll_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111lllllll_opy_(self, meta):
        self.meta = meta
    def bstack11l1111ll1_opy_(self, hooks):
        self.hooks = hooks
    def bstack1111llll1ll_opy_(self):
        bstack111l1111l11_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l11l1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬᶦ"): bstack111l1111l11_opy_,
            bstack1l11l1l_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬᶧ"): bstack111l1111l11_opy_,
            bstack1l11l1l_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩᶨ"): bstack111l1111l11_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l11l1l_opy_ (u"࡛ࠧ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷ࠾ࠥࠨᶩ") + key)
            setattr(self, key, val)
    def bstack1111lllll1l_opy_(self):
        return {
            bstack1l11l1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᶪ"): self.name,
            bstack1l11l1l_opy_ (u"ࠧࡣࡱࡧࡽࠬᶫ"): {
                bstack1l11l1l_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭ᶬ"): bstack1l11l1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᶭ"),
                bstack1l11l1l_opy_ (u"ࠪࡧࡴࡪࡥࠨᶮ"): self.code
            },
            bstack1l11l1l_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫᶯ"): self.scope,
            bstack1l11l1l_opy_ (u"ࠬࡺࡡࡨࡵࠪᶰ"): self.tags,
            bstack1l11l1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᶱ"): self.framework,
            bstack1l11l1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᶲ"): self.started_at
        }
    def bstack111l111l11l_opy_(self):
        return {
         bstack1l11l1l_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭ᶳ"): self.meta
        }
    def bstack111l111l111_opy_(self):
        return {
            bstack1l11l1l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡶࡺࡴࡐࡢࡴࡤࡱࠬᶴ"): {
                bstack1l11l1l_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠧᶵ"): self.bstack111l1111ll1_opy_
            }
        }
    def bstack1111llllll1_opy_(self, bstack111l1111l1l_opy_, details):
        step = next(filter(lambda st: st[bstack1l11l1l_opy_ (u"ࠫ࡮ࡪࠧᶶ")] == bstack111l1111l1l_opy_, self.meta[bstack1l11l1l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᶷ")]), None)
        step.update(details)
    def bstack1lll1lll1_opy_(self, bstack111l1111l1l_opy_):
        step = next(filter(lambda st: st[bstack1l11l1l_opy_ (u"࠭ࡩࡥࠩᶸ")] == bstack111l1111l1l_opy_, self.meta[bstack1l11l1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᶹ")]), None)
        step.update({
            bstack1l11l1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᶺ"): bstack1l1ll1l1l_opy_()
        })
    def bstack11l11111l1_opy_(self, bstack111l1111l1l_opy_, result, duration=None):
        bstack1l11ll1llll_opy_ = bstack1l1ll1l1l_opy_()
        if bstack111l1111l1l_opy_ is not None and self.meta.get(bstack1l11l1l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᶻ")):
            step = next(filter(lambda st: st[bstack1l11l1l_opy_ (u"ࠪ࡭ࡩ࠭ᶼ")] == bstack111l1111l1l_opy_, self.meta[bstack1l11l1l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᶽ")]), None)
            step.update({
                bstack1l11l1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᶾ"): bstack1l11ll1llll_opy_,
                bstack1l11l1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨᶿ"): duration if duration else bstack11l1l111111_opy_(step[bstack1l11l1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ᷀")], bstack1l11ll1llll_opy_),
                bstack1l11l1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ᷁"): result.result,
                bstack1l11l1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧ᷂ࠪ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack111l1111111_opy_):
        if self.meta.get(bstack1l11l1l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ᷃")):
            self.meta[bstack1l11l1l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ᷄")].append(bstack111l1111111_opy_)
        else:
            self.meta[bstack1l11l1l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ᷅")] = [ bstack111l1111111_opy_ ]
    def bstack1111lllllll_opy_(self):
        return {
            bstack1l11l1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ᷆"): self.bstack111l1l11ll_opy_(),
            **self.bstack1111lllll1l_opy_(),
            **self.bstack1111llll1ll_opy_(),
            **self.bstack111l111l11l_opy_()
        }
    def bstack111l111111l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l11l1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ᷇"): self.bstack1l11ll1llll_opy_,
            bstack1l11l1l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ᷈"): self.duration,
            bstack1l11l1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ᷉"): self.result.result
        }
        if data[bstack1l11l1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶ᷊ࠪ")] == bstack1l11l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᷋"):
            data[bstack1l11l1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ᷌")] = self.result.bstack1111ll11l1_opy_()
            data[bstack1l11l1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ᷍")] = [{bstack1l11l1l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧ᷎ࠪ"): self.result.bstack11ll111111l_opy_()}]
        return data
    def bstack111l1111lll_opy_(self):
        return {
            bstack1l11l1l_opy_ (u"ࠨࡷࡸ࡭ࡩ᷏࠭"): self.bstack111l1l11ll_opy_(),
            **self.bstack1111lllll1l_opy_(),
            **self.bstack1111llll1ll_opy_(),
            **self.bstack111l111111l_opy_(),
            **self.bstack111l111l11l_opy_()
        }
    def bstack111l11ll1l_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l11l1l_opy_ (u"ࠩࡖࡸࡦࡸࡴࡦࡦ᷐ࠪ") in event:
            return self.bstack1111lllllll_opy_()
        elif bstack1l11l1l_opy_ (u"ࠪࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ᷑") in event:
            return self.bstack111l1111lll_opy_()
    def bstack111l1lllll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l11ll1llll_opy_ = time if time else bstack1l1ll1l1l_opy_()
        self.duration = duration if duration else bstack11l1l111111_opy_(self.started_at, self.bstack1l11ll1llll_opy_)
        if result:
            self.result = result
class bstack11l111l11l_opy_(bstack111llll111_opy_):
    def __init__(self, hooks=[], bstack11l1111l11_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11l1111l11_opy_ = bstack11l1111l11_opy_
        super().__init__(*args, **kwargs, bstack1l1l1l1111_opy_=bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ᷒"))
    @classmethod
    def bstack111l11111ll_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l11l1l_opy_ (u"ࠬ࡯ࡤࠨᷓ"): id(step),
                bstack1l11l1l_opy_ (u"࠭ࡴࡦࡺࡷࠫᷔ"): step.name,
                bstack1l11l1l_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨᷕ"): step.keyword,
            })
        return bstack11l111l11l_opy_(
            **kwargs,
            meta={
                bstack1l11l1l_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩᷖ"): {
                    bstack1l11l1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᷗ"): feature.name,
                    bstack1l11l1l_opy_ (u"ࠪࡴࡦࡺࡨࠨᷘ"): feature.filename,
                    bstack1l11l1l_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᷙ"): feature.description
                },
                bstack1l11l1l_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧᷚ"): {
                    bstack1l11l1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᷛ"): scenario.name
                },
                bstack1l11l1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᷜ"): steps,
                bstack1l11l1l_opy_ (u"ࠨࡧࡻࡥࡲࡶ࡬ࡦࡵࠪᷝ"): bstack111l1l1l111_opy_(test)
            }
        )
    def bstack1111lllll11_opy_(self):
        return {
            bstack1l11l1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᷞ"): self.hooks
        }
    def bstack1111llll1l1_opy_(self):
        if self.bstack11l1111l11_opy_:
            return {
                bstack1l11l1l_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩᷟ"): self.bstack11l1111l11_opy_
            }
        return {}
    def bstack111l1111lll_opy_(self):
        return {
            **super().bstack111l1111lll_opy_(),
            **self.bstack1111lllll11_opy_()
        }
    def bstack1111lllllll_opy_(self):
        return {
            **super().bstack1111lllllll_opy_(),
            **self.bstack1111llll1l1_opy_()
        }
    def bstack111l1lllll_opy_(self):
        return bstack1l11l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ᷠ")
class bstack11l111llll_opy_(bstack111llll111_opy_):
    def __init__(self, hook_type, *args,bstack11l1111l11_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack111l11111l1_opy_ = None
        self.bstack11l1111l11_opy_ = bstack11l1111l11_opy_
        super().__init__(*args, **kwargs, bstack1l1l1l1111_opy_=bstack1l11l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᷡ"))
    def bstack111ll1llll_opy_(self):
        return self.hook_type
    def bstack111l111l1ll_opy_(self):
        return {
            bstack1l11l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᷢ"): self.hook_type
        }
    def bstack111l1111lll_opy_(self):
        return {
            **super().bstack111l1111lll_opy_(),
            **self.bstack111l111l1ll_opy_()
        }
    def bstack1111lllllll_opy_(self):
        return {
            **super().bstack1111lllllll_opy_(),
            bstack1l11l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬᷣ"): self.bstack111l11111l1_opy_,
            **self.bstack111l111l1ll_opy_()
        }
    def bstack111l1lllll_opy_(self):
        return bstack1l11l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪᷤ")
    def bstack11l111l111_opy_(self, bstack111l11111l1_opy_):
        self.bstack111l11111l1_opy_ = bstack111l11111l1_opy_