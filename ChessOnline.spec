# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Study\\LTM\\Nhom14-GameCoVua\\client\\main_enhanced.py'],
    pathex=[],
    binaries=[],
    datas=[('common', 'common'), ('client/ui', 'client/ui'), ('client/network', 'client/network')],
    hiddenimports=['tkinter', 'tkinter.ttk', 'PIL', 'PIL._tkinter_finder', 'chess', 'chess.engine', 'chess.pgn', 'pygame', 'pygame.mixer', 'numpy', 'plyer'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'scipy', 'pandas', 'IPython', 'jupyter', 'notebook', 'pytest', 'setuptools', 'wheel', 'pip'],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ChessOnline',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
