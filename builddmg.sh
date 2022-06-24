#!/bin/sh
mkdir -p dist/dmg
rm -r dist/dmg/*
cp -r "dist/Thanos.app" dist/dmg
test -f "dist/Thanos.dmg" && rm "dist/Thanos.dmg"
create-dmg \
  --volname "Thanos" \
  --volicon "icons/thanos.ico" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "Thanos.app" 175 120 \
  --hide-extension "Thanos.app" \
  --app-drop-link 425 120 \
  "dist/Thanos.dmg" \
  "dist/dmg/"