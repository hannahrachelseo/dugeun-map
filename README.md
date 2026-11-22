# 두근두근 · 우리만의 좌표 지도 데이터

두근두근 앱의 "우리만의 좌표" 지도(전국 시·도, 서울 구)가 이 저장소의 `mapdata.json`을 받아서 그려요.

- 원본: [vuski/admdongkor](https://github.com/vuski/admdongkor) 행정동 경계
- 매달 2일 GitHub Actions가 더 새 경계 파일이 있는지 확인하고, 있으면 `mapdata.json`을 다시 만들어 올려요.
- 앱은 켤 때 이 파일을 확인해서, 앱에 들어 있는 것보다 새 버전이면 자동으로 바꿔 써요.
