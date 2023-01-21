# -*- mode: python ; coding: utf-8 -*-
import os
import sys

local_lib = '/usr/local/lib/python3.10/dist-packages'

block_cipher = None

added_files = [
  (os.path.join(local_lib, 'django'), 'django'),
  (os.path.join(local_lib, 'rest_framework'), 'rest_framework'),
  (os.path.join(local_lib, 'corsheaders'), 'corsheaders'),
  (os.path.join(local_lib, 'Pillow.libs'), 'Pillow.libs'),
  (os.path.join(local_lib, 'PIL'), 'PIL'),
  (os.path.join(local_lib, 'django_filters'), 'django_filters'),
  (os.path.join(local_lib, 'itsdangerous'), 'itsdangerous'),
  (os.path.join(local_lib, 'shortuuid'), 'shortuuid'),
  (os.path.join(local_lib, 'pytz'), 'pytz'),
  (os.path.join(local_lib, 'sorl'), 'sorl'),
  (os.path.join(local_lib, 'tzdata'), 'tzdata'),
  

  ('app', 'app'),
  ('backend', 'backend'),
]

hide_imports = [
  "app",
  "backend",

  "django",
  "rest_framework",
  "corsheaders",
  "Pillow",
  "PIL",
  "django_filters",
  "itsdangerous",
  "shortuuid",
  "pytz",
  "tzdata",
]

manage_a = Analysis(['manage.py'],
             pathex=['/website', '/code'],
             binaries=[],
             datas=added_files,
             hiddenimports=hide_imports,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

manage_pyz = PYZ(manage_a.pure, manage_a.zipped_data,
             cipher=block_cipher)
manage_exe = EXE(manage_pyz,
          manage_a.scripts,
          [],
          exclude_binaries=True,
          name='manage',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )

manage_coll = COLLECT(manage_exe,
               manage_a.binaries,
               manage_a.zipfiles,
               manage_a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name=os.path.join('dist', 'manage'))
