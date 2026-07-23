# -*- mode: python ; coding: utf-8 -*-

import runpy
from pathlib import Path

from Service.constants import Constants


block_cipher = None
constants = Constants()
ui_compiler = runpy.run_path(str(Path(SPECPATH) / 'setup' / 'compile_ui.py'))
ui_compiler['compile_ui']()


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('./Common/*', './Common'),
        ('./Function/*', './Function'),
        ('./Service/*', './Service'),
        ('./Resource/checkmark.svg', './Resource'),
        ('./Resource/icon.icns', './Resource'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='CAU000',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CAU000',
)

app = BUNDLE(
    coll,
    name=f'{constants.PROCESS_NAME}.app',
    icon='Resource/icon.icns',
    bundle_identifier='com.knworks.CAU000',
    info_plist={
        'CFBundleName': constants.PROCESS_NAME,
        'CFBundleDisplayName': constants.PROCESS_NAME,
        'CFBundleShortVersionString': constants.APP_VERSION,
        'CFBundleVersion': constants.APP_VERSION,
        'NSRequiresAquaSystemAppearance': True,
    },
)
