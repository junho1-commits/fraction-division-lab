# -*- coding: utf-8 -*-
"""소스(app.source.html) → 배포용 index.html 생성.
   호스팅판에만 필요한 것(PWA 머리말, 앱 설치 버튼, 서비스 워커 등록, 검색 차단)을 붙인다.
   사용법:  python build.py
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, 'app.source.html')
OUT  = os.path.join(HERE, 'index.html')

s = io.open(SRC, encoding='utf-8').read()
MARK = '<div id="app">'
assert MARK in s, 'app.source.html 구조가 바뀌었습니다'
head, body = s.split(MARK, 1)
body = MARK + body

anchor = '<button class="iconbtn" id="btn-home">차시 목록</button>'
assert anchor in body
body = body.replace(anchor, '<button class="iconbtn" id="btn-install" hidden>앱 설치</button>\n    ' + anchor, 1)

TAIL = '''
<script>
/* ── 웹 앱 기능: 설치 버튼 + 오프라인 지원 ─────────────── */
(function(){
  var pending=null, btn=document.getElementById('btn-install');
  window.addEventListener('beforeinstallprompt',function(e){
    e.preventDefault(); pending=e; btn.hidden=false;
  });
  btn.addEventListener('click',function(){
    if(!pending)return;
    pending.prompt();
    pending.userChoice.then(function(){pending=null;btn.hidden=true;});
  });
  window.addEventListener('appinstalled',function(){btn.hidden=true;});

  var ok = location.protocol==='https:' || location.hostname==='localhost' || location.hostname==='127.0.0.1';
  if('serviceWorker' in navigator && ok){
    window.addEventListener('load',function(){
      navigator.serviceWorker.register('sw.js').catch(function(){});
    });
  }
})();
</script>
'''

doc = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex,nofollow,noarchive">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="초등학교 6학년 2학기 수학 1단원 분수의 나눗셈을 조작 활동으로 익히는 학습 앱. 여섯 차시를 구체물·그림·식·연습 네 단계로 공부합니다.">
<meta name="theme-color" content="#EDF3F6" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0A1820" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="분수 나눗셈">
<meta name="mobile-web-app-capable" content="yes">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/icon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon-180.png">
''' + head.strip() + '''
</head>
<body>
''' + body.rstrip() + TAIL + '''</body>
</html>
'''
io.open(OUT, 'w', encoding='utf-8', newline='\n').write(doc)
print('index.html OK - %d bytes' % len(doc))
