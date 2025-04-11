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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1lll1ll1ll_opy_, bstack1ll1lllll1_opy_
from bstack_utils.measure import measure
class bstack1l11ll1l_opy_:
  working_dir = os.getcwd()
  bstack111lll1l_opy_ = False
  config = {}
  bstack11l1lll11l1_opy_ = bstack1l11l1l_opy_ (u"ࠩࠪᱤ")
  binary_path = bstack1l11l1l_opy_ (u"ࠪࠫᱥ")
  bstack111llll11l1_opy_ = bstack1l11l1l_opy_ (u"ࠫࠬᱦ")
  bstack1l1ll1ll1_opy_ = False
  bstack11l1111l11l_opy_ = None
  bstack111llll1ll1_opy_ = {}
  bstack111lllll1l1_opy_ = 300
  bstack11l1111111l_opy_ = False
  logger = None
  bstack11l1111l1l1_opy_ = False
  bstack1ll11111ll_opy_ = False
  percy_build_id = None
  bstack111ll1ll11l_opy_ = bstack1l11l1l_opy_ (u"ࠬ࠭ᱧ")
  bstack111lll11l1l_opy_ = {
    bstack1l11l1l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ᱨ") : 1,
    bstack1l11l1l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨᱩ") : 2,
    bstack1l11l1l_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭ᱪ") : 3,
    bstack1l11l1l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩᱫ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111lll111ll_opy_(self):
    bstack11l1111l1ll_opy_ = bstack1l11l1l_opy_ (u"ࠪࠫᱬ")
    bstack111lll11l11_opy_ = sys.platform
    bstack111lllll1ll_opy_ = bstack1l11l1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᱭ")
    if re.match(bstack1l11l1l_opy_ (u"ࠧࡪࡡࡳࡹ࡬ࡲࢁࡳࡡࡤࠢࡲࡷࠧᱮ"), bstack111lll11l11_opy_) != None:
      bstack11l1111l1ll_opy_ = bstack11ll1llll11_opy_ + bstack1l11l1l_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳࡯ࡴࡺ࠱ࡾ࡮ࡶࠢᱯ")
      self.bstack111ll1ll11l_opy_ = bstack1l11l1l_opy_ (u"ࠧ࡮ࡣࡦࠫᱰ")
    elif re.match(bstack1l11l1l_opy_ (u"ࠣ࡯ࡶࡻ࡮ࡴࡼ࡮ࡵࡼࡷࢁࡳࡩ࡯ࡩࡺࢀࡨࡿࡧࡸ࡫ࡱࢀࡧࡩࡣࡸ࡫ࡱࢀࡼ࡯࡮ࡤࡧࡿࡩࡲࡩࡼࡸ࡫ࡱ࠷࠷ࠨᱱ"), bstack111lll11l11_opy_) != None:
      bstack11l1111l1ll_opy_ = bstack11ll1llll11_opy_ + bstack1l11l1l_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯ࡺ࡭ࡳ࠴ࡺࡪࡲࠥᱲ")
      bstack111lllll1ll_opy_ = bstack1l11l1l_opy_ (u"ࠥࡴࡪࡸࡣࡺ࠰ࡨࡼࡪࠨᱳ")
      self.bstack111ll1ll11l_opy_ = bstack1l11l1l_opy_ (u"ࠫࡼ࡯࡮ࠨᱴ")
    else:
      bstack11l1111l1ll_opy_ = bstack11ll1llll11_opy_ + bstack1l11l1l_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡲࡩ࡯ࡷࡻ࠲ࡿ࡯ࡰࠣᱵ")
      self.bstack111ll1ll11l_opy_ = bstack1l11l1l_opy_ (u"࠭࡬ࡪࡰࡸࡼࠬᱶ")
    return bstack11l1111l1ll_opy_, bstack111lllll1ll_opy_
  def bstack111ll1lllll_opy_(self):
    try:
      bstack111lll1ll11_opy_ = [os.path.join(expanduser(bstack1l11l1l_opy_ (u"ࠢࡿࠤᱷ")), bstack1l11l1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᱸ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack111lll1ll11_opy_:
        if(self.bstack111lll1lll1_opy_(path)):
          return path
      raise bstack1l11l1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨᱹ")
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡪࡰࡧࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡹࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠ࠮ࠢࡾࢁࠧᱺ").format(e))
  def bstack111lll1lll1_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack111ll1llll1_opy_(self, bstack111ll1l111l_opy_):
    return os.path.join(bstack111ll1l111l_opy_, self.bstack11l1lll11l1_opy_ + bstack1l11l1l_opy_ (u"ࠦ࠳࡫ࡴࡢࡩࠥᱻ"))
  def bstack111lll11111_opy_(self, bstack111ll1l111l_opy_, bstack111llll1l1l_opy_):
    if not bstack111llll1l1l_opy_: return
    try:
      bstack11l1111ll1l_opy_ = self.bstack111ll1llll1_opy_(bstack111ll1l111l_opy_)
      with open(bstack11l1111ll1l_opy_, bstack1l11l1l_opy_ (u"ࠧࡽࠢᱼ")) as f:
        f.write(bstack111llll1l1l_opy_)
        self.logger.debug(bstack1l11l1l_opy_ (u"ࠨࡓࡢࡸࡨࡨࠥࡴࡥࡸࠢࡈࡘࡦ࡭ࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡻࠥᱽ"))
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡦࡼࡥࠡࡶ࡫ࡩࠥ࡫ࡴࡢࡩ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢ᱾").format(e))
  def bstack111lllll11l_opy_(self, bstack111ll1l111l_opy_):
    try:
      bstack11l1111ll1l_opy_ = self.bstack111ll1llll1_opy_(bstack111ll1l111l_opy_)
      if os.path.exists(bstack11l1111ll1l_opy_):
        with open(bstack11l1111ll1l_opy_, bstack1l11l1l_opy_ (u"ࠣࡴࠥ᱿")) as f:
          bstack111llll1l1l_opy_ = f.read().strip()
          return bstack111llll1l1l_opy_ if bstack111llll1l1l_opy_ else None
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡉ࡙ࡧࡧ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᲀ").format(e))
  def bstack11l11111lll_opy_(self, bstack111ll1l111l_opy_, bstack11l1111l1ll_opy_):
    bstack111llll1lll_opy_ = self.bstack111lllll11l_opy_(bstack111ll1l111l_opy_)
    if bstack111llll1lll_opy_:
      try:
        bstack11l1111lll1_opy_ = self.bstack111lll1llll_opy_(bstack111llll1lll_opy_, bstack11l1111l1ll_opy_)
        if not bstack11l1111lll1_opy_:
          self.logger.debug(bstack1l11l1l_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢ࡬ࡷࠥࡻࡰࠡࡶࡲࠤࡩࡧࡴࡦࠢࠫࡉ࡙ࡧࡧࠡࡷࡱࡧ࡭ࡧ࡮ࡨࡧࡧ࠭ࠧᲁ"))
          return True
        self.logger.debug(bstack1l11l1l_opy_ (u"ࠦࡓ࡫ࡷࠡࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡹࡵࡪࡡࡵࡧࠥᲂ"))
        return False
      except Exception as e:
        self.logger.warn(bstack1l11l1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥ࡫ࡩࡨࡱࠠࡧࡱࡵࠤࡧ࡯࡮ࡢࡴࡼࠤࡺࡶࡤࡢࡶࡨࡷ࠱ࠦࡵࡴ࡫ࡱ࡫ࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡣ࡫ࡱࡥࡷࡿ࠺ࠡࡽࢀࠦᲃ").format(e))
    return False
  def bstack111lll1llll_opy_(self, bstack111llll1lll_opy_, bstack11l1111l1ll_opy_):
    try:
      headers = {
        bstack1l11l1l_opy_ (u"ࠨࡉࡧ࠯ࡑࡳࡳ࡫࠭ࡎࡣࡷࡧ࡭ࠨᲄ"): bstack111llll1lll_opy_
      }
      response = bstack1ll1lllll1_opy_(bstack1l11l1l_opy_ (u"ࠧࡈࡇࡗࠫᲅ"), bstack11l1111l1ll_opy_, {}, {bstack1l11l1l_opy_ (u"ࠣࡪࡨࡥࡩ࡫ࡲࡴࠤᲆ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1l11l1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡪࡴࡸࠠࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡵࡱࡦࡤࡸࡪࡹ࠺ࠡࡽࢀࠦᲇ").format(e))
  @measure(event_name=EVENTS.bstack11ll1lll111_opy_, stage=STAGE.bstack1l11l111ll_opy_)
  def bstack111llllllll_opy_(self, bstack11l1111l1ll_opy_, bstack111lllll1ll_opy_):
    try:
      bstack11l11111ll1_opy_ = self.bstack111ll1lllll_opy_()
      bstack111lll1111l_opy_ = os.path.join(bstack11l11111ll1_opy_, bstack1l11l1l_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰ࡽ࡭ࡵ࠭ᲈ"))
      bstack11l1111ll11_opy_ = os.path.join(bstack11l11111ll1_opy_, bstack111lllll1ll_opy_)
      if self.bstack11l11111lll_opy_(bstack11l11111ll1_opy_, bstack11l1111l1ll_opy_):
        if os.path.exists(bstack11l1111ll11_opy_):
          self.logger.info(bstack1l11l1l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࢁࡽ࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨᲉ").format(bstack11l1111ll11_opy_))
          return bstack11l1111ll11_opy_
        if os.path.exists(bstack111lll1111l_opy_):
          self.logger.info(bstack1l11l1l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡿ࡯ࡰࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡶࡰࡽ࡭ࡵࡶࡩ࡯ࡩࠥᲊ").format(bstack111lll1111l_opy_))
          return self.bstack111ll1ll111_opy_(bstack111lll1111l_opy_, bstack111lllll1ll_opy_)
      self.logger.info(bstack1l11l1l_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡷࡵ࡭ࠡࡽࢀࠦ᲋").format(bstack11l1111l1ll_opy_))
      response = bstack1ll1lllll1_opy_(bstack1l11l1l_opy_ (u"ࠧࡈࡇࡗࠫ᲌"), bstack11l1111l1ll_opy_, {}, {})
      if response.status_code == 200:
        bstack111llll11ll_opy_ = response.headers.get(bstack1l11l1l_opy_ (u"ࠣࡇࡗࡥ࡬ࠨ᲍"), bstack1l11l1l_opy_ (u"ࠤࠥ᲎"))
        if bstack111llll11ll_opy_:
          self.bstack111lll11111_opy_(bstack11l11111ll1_opy_, bstack111llll11ll_opy_)
        with open(bstack111lll1111l_opy_, bstack1l11l1l_opy_ (u"ࠪࡻࡧ࠭᲏")) as file:
          file.write(response.content)
        self.logger.info(bstack1l11l1l_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡢࡰࡧࠤࡸࡧࡶࡦࡦࠣࡥࡹࠦࡻࡾࠤᲐ").format(bstack111lll1111l_opy_))
        return self.bstack111ll1ll111_opy_(bstack111lll1111l_opy_, bstack111lllll1ll_opy_)
      else:
        raise(bstack1l11l1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡸ࡭࡫ࠠࡧ࡫࡯ࡩ࠳ࠦࡓࡵࡣࡷࡹࡸࠦࡣࡰࡦࡨ࠾ࠥࢁࡽࠣᲑ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻ࠽ࠤࢀࢃࠢᲒ").format(e))
  def bstack111lll11ll1_opy_(self, bstack11l1111l1ll_opy_, bstack111lllll1ll_opy_):
    try:
      retry = 2
      bstack11l1111ll11_opy_ = None
      bstack111lllll111_opy_ = False
      while retry > 0:
        bstack11l1111ll11_opy_ = self.bstack111llllllll_opy_(bstack11l1111l1ll_opy_, bstack111lllll1ll_opy_)
        bstack111lllll111_opy_ = self.bstack111lll1ll1l_opy_(bstack11l1111l1ll_opy_, bstack111lllll1ll_opy_, bstack11l1111ll11_opy_)
        if bstack111lllll111_opy_:
          break
        retry -= 1
      return bstack11l1111ll11_opy_, bstack111lllll111_opy_
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡺࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡰࡢࡶ࡫ࠦᲓ").format(e))
    return bstack11l1111ll11_opy_, False
  def bstack111lll1ll1l_opy_(self, bstack11l1111l1ll_opy_, bstack111lllll1ll_opy_, bstack11l1111ll11_opy_, bstack11l1111llll_opy_ = 0):
    if bstack11l1111llll_opy_ > 1:
      return False
    if bstack11l1111ll11_opy_ == None or os.path.exists(bstack11l1111ll11_opy_) == False:
      self.logger.warn(bstack1l11l1l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡱࡣࡷ࡬ࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠭ࠢࡵࡩࡹࡸࡹࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨᲔ"))
      return False
    bstack111lll111l1_opy_ = bstack1l11l1l_opy_ (u"ࠤࡡ࠲࠯ࡆࡰࡦࡴࡦࡽࡡ࠵ࡣ࡭࡫ࠣࡠࡩ࠴࡜ࡥ࠭࠱ࡠࡩ࠱ࠢᲕ")
    command = bstack1l11l1l_opy_ (u"ࠪࡿࢂࠦ࠭࠮ࡸࡨࡶࡸ࡯࡯࡯ࠩᲖ").format(bstack11l1111ll11_opy_)
    bstack111ll1l1lll_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111lll111l1_opy_, bstack111ll1l1lll_opy_) != None:
      return True
    else:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡺࡪࡸࡳࡪࡱࡱࠤࡨ࡮ࡥࡤ࡭ࠣࡪࡦ࡯࡬ࡦࡦࠥᲗ"))
      return False
  def bstack111ll1ll111_opy_(self, bstack111lll1111l_opy_, bstack111lllll1ll_opy_):
    try:
      working_dir = os.path.dirname(bstack111lll1111l_opy_)
      shutil.unpack_archive(bstack111lll1111l_opy_, working_dir)
      bstack11l1111ll11_opy_ = os.path.join(working_dir, bstack111lllll1ll_opy_)
      os.chmod(bstack11l1111ll11_opy_, 0o755)
      return bstack11l1111ll11_opy_
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡷࡱࡾ࡮ࡶࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨᲘ"))
  def bstack111ll1l1l1l_opy_(self):
    try:
      bstack111ll1ll1ll_opy_ = self.config.get(bstack1l11l1l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᲙ"))
      bstack111ll1l1l1l_opy_ = bstack111ll1ll1ll_opy_ or (bstack111ll1ll1ll_opy_ is None and self.bstack111lll1l_opy_)
      if not bstack111ll1l1l1l_opy_ or self.config.get(bstack1l11l1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᲚ"), None) not in bstack11ll1ll11ll_opy_:
        return False
      self.bstack1l1ll1ll1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᲛ").format(e))
  def bstack11l11111111_opy_(self):
    try:
      bstack11l11111111_opy_ = self.percy_capture_mode
      return bstack11l11111111_opy_
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼࠤࡨࡧࡰࡵࡷࡵࡩࠥࡳ࡯ࡥࡧ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᲜ").format(e))
  def init(self, bstack111lll1l_opy_, config, logger):
    self.bstack111lll1l_opy_ = bstack111lll1l_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111ll1l1l1l_opy_():
      return
    self.bstack111llll1ll1_opy_ = config.get(bstack1l11l1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᲝ"), {})
    self.percy_capture_mode = config.get(bstack1l11l1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧᲞ"))
    try:
      bstack11l1111l1ll_opy_, bstack111lllll1ll_opy_ = self.bstack111lll111ll_opy_()
      self.bstack11l1lll11l1_opy_ = bstack111lllll1ll_opy_
      bstack11l1111ll11_opy_, bstack111lllll111_opy_ = self.bstack111lll11ll1_opy_(bstack11l1111l1ll_opy_, bstack111lllll1ll_opy_)
      if bstack111lllll111_opy_:
        self.binary_path = bstack11l1111ll11_opy_
        thread = Thread(target=self.bstack111lll11lll_opy_)
        thread.start()
      else:
        self.bstack11l1111l1l1_opy_ = True
        self.logger.error(bstack1l11l1l_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡰࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡪࡴࡻ࡮ࡥࠢ࠰ࠤࢀࢃࠬࠡࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡔࡪࡸࡣࡺࠤᲟ").format(bstack11l1111ll11_opy_))
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᲠ").format(e))
  def bstack111ll1lll1l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1l11l1l_opy_ (u"ࠧ࡭ࡱࡪࠫᲡ"), bstack1l11l1l_opy_ (u"ࠨࡲࡨࡶࡨࡿ࠮࡭ࡱࡪࠫᲢ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1l11l1l_opy_ (u"ࠤࡓࡹࡸ࡮ࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࡹࠠࡢࡶࠣࡿࢂࠨᲣ").format(logfile))
      self.bstack111llll11l1_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡦࡶࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࠦࡰࡢࡶ࡫࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᲤ").format(e))
  @measure(event_name=EVENTS.bstack11ll1ll1ll1_opy_, stage=STAGE.bstack1l11l111ll_opy_)
  def bstack111lll11lll_opy_(self):
    bstack111lllllll1_opy_ = self.bstack111llll111l_opy_()
    if bstack111lllllll1_opy_ == None:
      self.bstack11l1111l1l1_opy_ = True
      self.logger.error(bstack1l11l1l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡸࡴࡱࡥ࡯ࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠢᲥ"))
      return False
    command_args = [bstack1l11l1l_opy_ (u"ࠧࡧࡰࡱ࠼ࡨࡼࡪࡩ࠺ࡴࡶࡤࡶࡹࠨᲦ") if self.bstack111lll1l_opy_ else bstack1l11l1l_opy_ (u"࠭ࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠪᲧ")]
    bstack11l111l1l1l_opy_ = self.bstack111lll1l1ll_opy_()
    if bstack11l111l1l1l_opy_ != None:
      command_args.append(bstack1l11l1l_opy_ (u"ࠢ࠮ࡥࠣࡿࢂࠨᲨ").format(bstack11l111l1l1l_opy_))
    env = os.environ.copy()
    env[bstack1l11l1l_opy_ (u"ࠣࡒࡈࡖࡈ࡟࡟ࡕࡑࡎࡉࡓࠨᲩ")] = bstack111lllllll1_opy_
    env[bstack1l11l1l_opy_ (u"ࠤࡗࡌࡤࡈࡕࡊࡎࡇࡣ࡚࡛ࡉࡅࠤᲪ")] = os.environ.get(bstack1l11l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᲫ"), bstack1l11l1l_opy_ (u"ࠫࠬᲬ"))
    bstack11l111111l1_opy_ = [self.binary_path]
    self.bstack111ll1lll1l_opy_()
    self.bstack11l1111l11l_opy_ = self.bstack111ll1l1ll1_opy_(bstack11l111111l1_opy_ + command_args, env)
    self.logger.debug(bstack1l11l1l_opy_ (u"࡙ࠧࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠨᲭ"))
    bstack11l1111llll_opy_ = 0
    while self.bstack11l1111l11l_opy_.poll() == None:
      bstack111llll1l11_opy_ = self.bstack111lll1l11l_opy_()
      if bstack111llll1l11_opy_:
        self.logger.debug(bstack1l11l1l_opy_ (u"ࠨࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠤᲮ"))
        self.bstack11l1111111l_opy_ = True
        return True
      bstack11l1111llll_opy_ += 1
      self.logger.debug(bstack1l11l1l_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡒࡦࡶࡵࡽࠥ࠳ࠠࡼࡿࠥᲯ").format(bstack11l1111llll_opy_))
      time.sleep(2)
    self.logger.error(bstack1l11l1l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡉࡥ࡮ࡲࡥࡥࠢࡤࡪࡹ࡫ࡲࠡࡽࢀࠤࡦࡺࡴࡦ࡯ࡳࡸࡸࠨᲰ").format(bstack11l1111llll_opy_))
    self.bstack11l1111l1l1_opy_ = True
    return False
  def bstack111lll1l11l_opy_(self, bstack11l1111llll_opy_ = 0):
    if bstack11l1111llll_opy_ > 10:
      return False
    try:
      bstack111ll1lll11_opy_ = os.environ.get(bstack1l11l1l_opy_ (u"ࠩࡓࡉࡗࡉ࡙ࡠࡕࡈࡖ࡛ࡋࡒࡠࡃࡇࡈࡗࡋࡓࡔࠩᲱ"), bstack1l11l1l_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡰࡴࡩࡡ࡭ࡪࡲࡷࡹࡀ࠵࠴࠵࠻ࠫᲲ"))
      bstack111ll1ll1l1_opy_ = bstack111ll1lll11_opy_ + bstack11ll1ll1111_opy_
      response = requests.get(bstack111ll1ll1l1_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1l11l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࠪᲳ"), {}).get(bstack1l11l1l_opy_ (u"ࠬ࡯ࡤࠨᲴ"), None)
      return True
    except:
      self.logger.debug(bstack1l11l1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡵࡣࡤࡷࡵࡶࡪࡪࠠࡸࡪ࡬ࡰࡪࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣ࡬ࡪࡧ࡬ࡵࡪࠣࡧ࡭࡫ࡣ࡬ࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠦᲵ"))
      return False
  def bstack111llll111l_opy_(self):
    bstack11l111111ll_opy_ = bstack1l11l1l_opy_ (u"ࠧࡢࡲࡳࠫᲶ") if self.bstack111lll1l_opy_ else bstack1l11l1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪᲷ")
    bstack11l1111l111_opy_ = bstack1l11l1l_opy_ (u"ࠤࡸࡲࡩ࡫ࡦࡪࡰࡨࡨࠧᲸ") if self.config.get(bstack1l11l1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᲹ")) is None else True
    bstack11ll111ll11_opy_ = bstack1l11l1l_opy_ (u"ࠦࡦࡶࡩ࠰ࡣࡳࡴࡤࡶࡥࡳࡥࡼ࠳࡬࡫ࡴࡠࡲࡵࡳ࡯࡫ࡣࡵࡡࡷࡳࡰ࡫࡮ࡀࡰࡤࡱࡪࡃࡻࡾࠨࡷࡽࡵ࡫࠽ࡼࡿࠩࡴࡪࡸࡣࡺ࠿ࡾࢁࠧᲺ").format(self.config[bstack1l11l1l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ᲻")], bstack11l111111ll_opy_, bstack11l1111l111_opy_)
    if self.percy_capture_mode:
      bstack11ll111ll11_opy_ += bstack1l11l1l_opy_ (u"ࠨࠦࡱࡧࡵࡧࡾࡥࡣࡢࡲࡷࡹࡷ࡫࡟࡮ࡱࡧࡩࡂࢁࡽࠣ᲼").format(self.percy_capture_mode)
    uri = bstack1lll1ll1ll_opy_(bstack11ll111ll11_opy_)
    try:
      response = bstack1ll1lllll1_opy_(bstack1l11l1l_opy_ (u"ࠧࡈࡇࡗࠫᲽ"), uri, {}, {bstack1l11l1l_opy_ (u"ࠨࡣࡸࡸ࡭࠭Ჾ"): (self.config[bstack1l11l1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᲿ")], self.config[bstack1l11l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭᳀")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1l1ll1ll1_opy_ = data.get(bstack1l11l1l_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ᳁"))
        self.percy_capture_mode = data.get(bstack1l11l1l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡣࡨࡧࡰࡵࡷࡵࡩࡤࡳ࡯ࡥࡧࠪ᳂"))
        os.environ[bstack1l11l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࠫ᳃")] = str(self.bstack1l1ll1ll1_opy_)
        os.environ[bstack1l11l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࡤࡉࡁࡑࡖࡘࡖࡊࡥࡍࡐࡆࡈࠫ᳄")] = str(self.percy_capture_mode)
        if bstack11l1111l111_opy_ == bstack1l11l1l_opy_ (u"ࠣࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧࠦ᳅") and str(self.bstack1l1ll1ll1_opy_).lower() == bstack1l11l1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ᳆"):
          self.bstack1ll11111ll_opy_ = True
        if bstack1l11l1l_opy_ (u"ࠥࡸࡴࡱࡥ࡯ࠤ᳇") in data:
          return data[bstack1l11l1l_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥ᳈")]
        else:
          raise bstack1l11l1l_opy_ (u"࡚ࠬ࡯࡬ࡧࡱࠤࡓࡵࡴࠡࡈࡲࡹࡳࡪࠠ࠮ࠢࡾࢁࠬ᳉").format(data)
      else:
        raise bstack1l11l1l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡲࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡶࡸࡦࡺࡵࡴࠢ࠰ࠤࢀࢃࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡆࡴࡪࡹࠡ࠯ࠣࡿࢂࠨ᳊").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡱࡴࡲ࡮ࡪࡩࡴࠣ᳋").format(e))
  def bstack111lll1l1ll_opy_(self):
    bstack11l11111l11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11l1l_opy_ (u"ࠣࡲࡨࡶࡨࡿࡃࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠦ᳌"))
    try:
      if bstack1l11l1l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪ᳍") not in self.bstack111llll1ll1_opy_:
        self.bstack111llll1ll1_opy_[bstack1l11l1l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫ᳎")] = 2
      with open(bstack11l11111l11_opy_, bstack1l11l1l_opy_ (u"ࠫࡼ࠭᳏")) as fp:
        json.dump(self.bstack111llll1ll1_opy_, fp)
      return bstack11l11111l11_opy_
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡥࡵࡩࡦࡺࡥࠡࡲࡨࡶࡨࡿࠠࡤࡱࡱࡪ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ᳐").format(e))
  def bstack111ll1l1ll1_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111ll1ll11l_opy_ == bstack1l11l1l_opy_ (u"࠭ࡷࡪࡰࠪ᳑"):
        bstack111llll1111_opy_ = [bstack1l11l1l_opy_ (u"ࠧࡤ࡯ࡧ࠲ࡪࡾࡥࠨ᳒"), bstack1l11l1l_opy_ (u"ࠨ࠱ࡦࠫ᳓")]
        cmd = bstack111llll1111_opy_ + cmd
      cmd = bstack1l11l1l_opy_ (u"᳔ࠩࠣࠫ").join(cmd)
      self.logger.debug(bstack1l11l1l_opy_ (u"ࠥࡖࡺࡴ࡮ࡪࡰࡪࠤࢀࢃ᳕ࠢ").format(cmd))
      with open(self.bstack111llll11l1_opy_, bstack1l11l1l_opy_ (u"ࠦࡦࠨ᳖")) as bstack111llllll1l_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack111llllll1l_opy_, text=True, stderr=bstack111llllll1l_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack11l1111l1l1_opy_ = True
      self.logger.error(bstack1l11l1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾࠦࡷࡪࡶ࡫ࠤࡨࡳࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃ᳗ࠢ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11l1111111l_opy_:
        self.logger.info(bstack1l11l1l_opy_ (u"ࠨࡓࡵࡱࡳࡴ࡮ࡴࡧࠡࡒࡨࡶࡨࡿ᳘ࠢ"))
        cmd = [self.binary_path, bstack1l11l1l_opy_ (u"ࠢࡦࡺࡨࡧ࠿ࡹࡴࡰࡲ᳙ࠥ")]
        self.bstack111ll1l1ll1_opy_(cmd)
        self.bstack11l1111111l_opy_ = False
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺ࡯ࡱࠢࡶࡩࡸࡹࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡥࡲࡱࡲࡧ࡮ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣ᳚").format(cmd, e))
  def bstack1l11111ll1_opy_(self):
    if not self.bstack1l1ll1ll1_opy_:
      return
    try:
      bstack111ll1l11l1_opy_ = 0
      while not self.bstack11l1111111l_opy_ and bstack111ll1l11l1_opy_ < self.bstack111lllll1l1_opy_:
        if self.bstack11l1111l1l1_opy_:
          self.logger.info(bstack1l11l1l_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡵࡨࡸࡺࡶࠠࡧࡣ࡬ࡰࡪࡪࠢ᳛"))
          return
        time.sleep(1)
        bstack111ll1l11l1_opy_ += 1
      os.environ[bstack1l11l1l_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡅࡉࡘ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎ᳜ࠩ")] = str(self.bstack11l11111l1l_opy_())
      self.logger.info(bstack1l11l1l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡷࡪࡺࡵࡱࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨ᳝ࠧ"))
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ᳞").format(e))
  def bstack11l11111l1l_opy_(self):
    if self.bstack111lll1l_opy_:
      return
    try:
      bstack111ll1l11ll_opy_ = [platform[bstack1l11l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨ᳟ࠫ")].lower() for platform in self.config.get(bstack1l11l1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ᳠"), [])]
      bstack111lll1l1l1_opy_ = sys.maxsize
      bstack111llllll11_opy_ = bstack1l11l1l_opy_ (u"ࠨࠩ᳡")
      for browser in bstack111ll1l11ll_opy_:
        if browser in self.bstack111lll11l1l_opy_:
          bstack111lll1l111_opy_ = self.bstack111lll11l1l_opy_[browser]
        if bstack111lll1l111_opy_ < bstack111lll1l1l1_opy_:
          bstack111lll1l1l1_opy_ = bstack111lll1l111_opy_
          bstack111llllll11_opy_ = browser
      return bstack111llllll11_opy_
    except Exception as e:
      self.logger.error(bstack1l11l1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡦࡪࡹࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿ᳢ࠥ").format(e))
  @classmethod
  def bstack1l1ll1l11_opy_(self):
    return os.getenv(bstack1l11l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨ᳣"), bstack1l11l1l_opy_ (u"ࠫࡋࡧ࡬ࡴࡧ᳤ࠪ")).lower()
  @classmethod
  def bstack1lll11lll1_opy_(self):
    return os.getenv(bstack1l11l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆ᳥ࠩ"), bstack1l11l1l_opy_ (u"᳦࠭ࠧ"))
  @classmethod
  def bstack1l1ll1lll1l_opy_(cls, value):
    cls.bstack1ll11111ll_opy_ = value
  @classmethod
  def bstack111ll1l1111_opy_(cls):
    return cls.bstack1ll11111ll_opy_
  @classmethod
  def bstack1l1ll1ll11l_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack111ll1l1l11_opy_(cls):
    return cls.percy_build_id