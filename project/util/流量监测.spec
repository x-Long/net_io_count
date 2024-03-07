# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['流量监测.py'],
             pathex=[],
             binaries=[],
             datas=[('.\\project\\asset\\*', '.\\project\\asset'), ('.\\pyd_cache\\', '.\\project')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
#**********************************************************************
# from pprint import pprint
# pprint(a.pure)

project_name = "net_io_count"

un_embed_exe = [x[1] for x in a.pure if project_name in x[1]]
print(un_embed_exe)

a.pure = [x for x in a.pure if project_name not in x[1]]
#**********************************************************************
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='流量监测',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='流量监测')
