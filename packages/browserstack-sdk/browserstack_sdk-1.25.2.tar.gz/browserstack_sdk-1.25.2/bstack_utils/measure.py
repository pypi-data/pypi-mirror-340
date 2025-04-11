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
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1l111l1ll_opy_ import get_logger
from bstack_utils.bstack1111l11l_opy_ import bstack1lllll11l1l_opy_
bstack1111l11l_opy_ = bstack1lllll11l1l_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1111lll1l_opy_: Optional[str] = None):
    bstack1l11l1l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡇࡩࡨࡵࡲࡢࡶࡲࡶࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡺࡨࡦࠢࡶࡸࡦࡸࡴࠡࡶ࡬ࡱࡪࠦ࡯ࡧࠢࡤࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࡡ࡭ࡱࡱ࡫ࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࠢࡱࡥࡲ࡫ࠠࡢࡰࡧࠤࡸࡺࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࠤࠥࠦᰗ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll1ll1ll1l_opy_: str = bstack1111l11l_opy_.bstack11lllll1111_opy_(label)
            start_mark: str = label + bstack1l11l1l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᰘ")
            end_mark: str = label + bstack1l11l1l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᰙ")
            result = None
            try:
                if stage.value == STAGE.bstack1ll1l11ll_opy_.value:
                    bstack1111l11l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1111l11l_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1111lll1l_opy_)
                elif stage.value == STAGE.bstack1l11l111ll_opy_.value:
                    start_mark: str = bstack1ll1ll1ll1l_opy_ + bstack1l11l1l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᰚ")
                    end_mark: str = bstack1ll1ll1ll1l_opy_ + bstack1l11l1l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᰛ")
                    bstack1111l11l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1111l11l_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1111lll1l_opy_)
            except Exception as e:
                bstack1111l11l_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1111lll1l_opy_)
            return result
        return wrapper
    return decorator