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
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack1l111l1ll_opy_ import get_logger
logger = get_logger(__name__)
bstack111ll11111l_opy_: Dict[str, float] = {}
bstack111ll111111_opy_: List = []
bstack111ll1111l1_opy_ = 5
bstack1111l1l1_opy_ = os.path.join(os.getcwd(), bstack1l11l1l_opy_ (u"ࠨ࡮ࡲ࡫᳨ࠬ"), bstack1l11l1l_opy_ (u"ࠩ࡮ࡩࡾ࠳࡭ࡦࡶࡵ࡭ࡨࡹ࠮࡫ࡵࡲࡲࠬᳩ"))
logging.getLogger(bstack1l11l1l_opy_ (u"ࠪࡪ࡮ࡲࡥ࡭ࡱࡦ࡯ࠬᳪ")).setLevel(logging.WARNING)
lock = FileLock(bstack1111l1l1_opy_+bstack1l11l1l_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥᳫ"))
class bstack111l1llllll_opy_:
    duration: float
    name: str
    startTime: float
    worker: int
    status: bool
    failure: str
    details: Optional[str]
    entryType: str
    platform: Optional[int]
    command: Optional[str]
    hookType: Optional[str]
    cli: Optional[bool]
    def __init__(self, duration: float, name: str, start_time: float, bstack111l1lll11l_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack111l1lll11l_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1l11l1l_opy_ (u"ࠧࡳࡥࡢࡵࡸࡶࡪࠨᳬ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1lllll11l1l_opy_:
    global bstack111ll11111l_opy_
    @staticmethod
    def bstack1ll11llll11_opy_(key: str):
        bstack1ll1ll1ll1l_opy_ = bstack1lllll11l1l_opy_.bstack11lllll1111_opy_(key)
        bstack1lllll11l1l_opy_.mark(bstack1ll1ll1ll1l_opy_+bstack1l11l1l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ᳭"))
        return bstack1ll1ll1ll1l_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack111ll11111l_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1l11l1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࡀࠠࡼࡿࠥᳮ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1lllll11l1l_opy_.mark(end)
            bstack1lllll11l1l_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1l11l1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳ࠻ࠢࡾࢁࠧᳯ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack111ll11111l_opy_ or end not in bstack111ll11111l_opy_:
                logger.debug(bstack1l11l1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸࡺࡡࡳࡶࠣ࡯ࡪࡿࠠࡸ࡫ࡷ࡬ࠥࡼࡡ࡭ࡷࡨࠤࢀࢃࠠࡰࡴࠣࡩࡳࡪࠠ࡬ࡧࡼࠤࡼ࡯ࡴࡩࠢࡹࡥࡱࡻࡥࠡࡽࢀࠦᳰ").format(start,end))
                return
            duration: float = bstack111ll11111l_opy_[end] - bstack111ll11111l_opy_[start]
            bstack111l1lllll1_opy_ = os.environ.get(bstack1l11l1l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡌࡗࡤࡘࡕࡏࡐࡌࡒࡌࠨᳱ"), bstack1l11l1l_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥᳲ")).lower() == bstack1l11l1l_opy_ (u"ࠧࡺࡲࡶࡧࠥᳳ")
            bstack111l1llll1l_opy_: bstack111l1llllll_opy_ = bstack111l1llllll_opy_(duration, label, bstack111ll11111l_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack1l11l1l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨ᳴"), 0), command, test_name, hook_type, bstack111l1lllll1_opy_)
            del bstack111ll11111l_opy_[start]
            del bstack111ll11111l_opy_[end]
            bstack1lllll11l1l_opy_.bstack111l1llll11_opy_(bstack111l1llll1l_opy_)
        except Exception as e:
            logger.debug(bstack1l11l1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡥࡢࡵࡸࡶ࡮ࡴࡧࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥᳵ").format(e))
    @staticmethod
    def bstack111l1llll11_opy_(bstack111l1llll1l_opy_):
        os.makedirs(os.path.dirname(bstack1111l1l1_opy_)) if not os.path.exists(os.path.dirname(bstack1111l1l1_opy_)) else None
        bstack1lllll11l1l_opy_.bstack111l1lll1ll_opy_()
        try:
            with lock:
                with open(bstack1111l1l1_opy_, bstack1l11l1l_opy_ (u"ࠣࡴ࠮ࠦᳶ"), encoding=bstack1l11l1l_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ᳷")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack111l1llll1l_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack111l1lll1l1_opy_:
            logger.debug(bstack1l11l1l_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠤࢀࢃࠢ᳸").format(bstack111l1lll1l1_opy_))
            with lock:
                with open(bstack1111l1l1_opy_, bstack1l11l1l_opy_ (u"ࠦࡼࠨ᳹"), encoding=bstack1l11l1l_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᳺ")) as file:
                    data = [bstack111l1llll1l_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack1l11l1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࠦࡡࡱࡲࡨࡲࡩࠦࡻࡾࠤ᳻").format(str(e)))
        finally:
            if os.path.exists(bstack1111l1l1_opy_+bstack1l11l1l_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨ᳼")):
                os.remove(bstack1111l1l1_opy_+bstack1l11l1l_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢ᳽"))
    @staticmethod
    def bstack111l1lll1ll_opy_():
        attempt = 0
        while (attempt < bstack111ll1111l1_opy_):
            attempt += 1
            if os.path.exists(bstack1111l1l1_opy_+bstack1l11l1l_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫ࠣ᳾")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11lllll1111_opy_(label: str) -> str:
        try:
            return bstack1l11l1l_opy_ (u"ࠥࡿࢂࡀࡻࡾࠤ᳿").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1l11l1l_opy_ (u"ࠦࡊࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᴀ").format(e))