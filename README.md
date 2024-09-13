# README
- 주의: 모든 raw 테이블에 랜덤하게 누락된 행들이 있기 때문에 이를 항상 주의해야 한다.
- config.py에서 data_dir 변수가 raw 테이블들이 있는 data 폴더를 가리키도록 설정해야 한다.

## Part 1. Level Up 패널 데이터 생성

### 01_create_levelup_panel.ipynb
- sample selection을 실시해서 일부 플레이어들을 분석 대상에서 제외한다.
    - 캐릭터를 2개 이상 생성한 플레이어는 우선 제외했다.
- 각 행이 (레드스완 / 2021-11-01 / 레벨1->2) 와 같이 캐릭터별 레벨업 내역을 나타내도록 분석의 기초가 되는 levelups_ref 테이블을 만든다.
- 로그인, 광고 시청, 인앱결제 등의 추가적인 테이블들을 활용해서 각 레벨에서 레벨업하는 동안 관찰된 feature를 추가한다.
    - interval 변수는 직전 레벨업으로부터 현 레벨업까지 걸린 총 hour를 가리키며, 이는 playing time과 non-playing time을 모두 포함한다.
        - 참고로 로그인 로그가 있어도 로그아웃 로그가 없기 때문에 actual playing time은 관찰할 수가 없다.
    - interval_cum 변수는 interval의 cumulative sum이다.
- 기본적인 feature들이 추가된 levelups_ref 테이블을 levelups_panel_1.csv로 저장한다.


## Part 2. Level Up 패널 데이터에 Play Hours 추가
- 각 레벨에서의 playing time과 non-playing time을 분리해보고자 했다.
    - 특히 main quest와 side quest를 플레이한 시간들을 측정하고자 했다.
- 보스 토벌/주간 던전/천공의 탑 등 side quests의 경우 플레이 타임이 짧기 때문에 비교적 정확하게 playing time을 정확하게 계산할 수 있다.
- 하지만 main quest는 시작 시간과 종료 시간이 있더라도 중간중간 플레이를 멈춘 시간을 알 수 없다는 한계점이 있다.

### 02_1_refine_stages (lab).ipynb
- 퀘스트 수행 내역이 저장된 characters_stages_n.csv 파일들은 기본적으로 용량이 매우 크다.
- 따라서 raw 테이블을 불러온 다음에 selected players에 한하는 로그들만 선택해서 stages.csv 파일로 저장한다.

### 02_2_process_side_quests (lab).ipynb
- stages.csv 파일을 이용해서 side quest 플레이 타임을 계산한다.
    - 단, 주의할 점이 플레이 도중 레벨업이 (그것도 연속해서) 일어날 수 있다는 점이다.
- 각 side quest별 플레이 시간을 새로운 변수로 가공해서 levelups_panel_1.csv에 붙인 다음 levelups_panel_2.csv로 저장한다.
    - playtime_boss: hours of playing 보스 토벌
    - playtime_dungeon: hours of playing 주간 던전
    - playtime_tower: hours of playing 천공의 탑
    - playtime_pvp: hours of playing PVP
    - playtime_farm: hours of playing 파밍 필드
    - playtime_survival: hours of playing 허상의 결계
    - playtime_side: 위 6개 side quest playing time의 sum

### 02_3_process_main_quests (lab) (work-in-progress).ipynb (보류)
- stages.csv 파일과 다른 테이블들을 이용해서 main quest 플레이 타임을 proxy한다.
- 전술했듯이 중간중간 게임을 멈추고 앱을 나간 시간을 알지 못하는 한계점이 있다.
- 이에 따라 현재의 아이디어는 각 로그인 이후 다음 로그인이 있기 전 가장 마지막으로 관찰된 transaction timestamp를 로그아웃 시점으로 생각하는 것이다.
    - 그리고 이 estimated 시간에서 side quest 플레이 타임을 제외하면 아마도 main quest 플레이 타임에 가까운 시간을 구할 수 있을 것이다.
- levelups_panel_2.csv에 playtime_main 변수를 추가하고 levelups_panel_3.csv로 저장한다.
- 현재 계산된 playtime_main에 지나치게 큰 값이 많이 섞여있어서 이 작업은 잠시 보류한다.

### 02_4_process_final_touch.ipynb
- 앞서 가공한 변수들에 문제가 없는지 체크한다.
- 그리고 levelups_ref 테이블에서 각 행이 censored 되었는지 체크해서 status 변수로 표기한다.
    - 레벨업이 study period의 마지막 week에 일어났다면 아직 플레이 중이라고 임의로 인식했다. (개선 가능성 있음)
- status와 playing time이 추가된 levelups_ref 테이블을 최종적으로 levelups_panel_4.csv로 저장한다.
    - 현재 버전에서는 02_3 단계에서 생성한 playtime_main은 활용하지 않았다.


## Part 3. Binger vs. Non-Binger 분류
- 가장 중요하게 binger를 구분하는 작업이다.
- 가장 첫 세션에서 몇 시간 연속해서 플레이했는지 정보를 바탕으로 binger를 분류하고자 했으나, 전술했듯이 actual playing time은 관찰할 수가 없다.
- 대신 레벨업 내역이 있으니 가장 첫 세션에서 도달한 레벨을 바탕으로 높으면 binger, 낮으면 non-binger로 분류하고자 했다.

### 03_1_process_first_session_level.ipynb
- 가장 첫 세션에서 (또는 가장 최초 로그인 이후 다음 로그인 이전까지) 도달한 레벨을 first_session_level 변수로 표기한다.
    - 단, 1시간 이내 발생한 로그인은 무시해서 다음 로그인은 최소 1시간 뒤에 발생한 로그인으로 인식했다.
- first_session_level 변수를 추가한 levelups_ref 테이블을 levelups_panel_5.csv로 저장한다.

### 03_2_binger_classification.ipynb
- 대략 레벨 50까지 도달하는 데 1시간 30분이 걸리는 것을 확인했다.
    - 게임을 설치하고 가장 첫 세션에서 레벨 50을 넘긴 약 22%의 플레이어들을 binger로 분류했다. (추후 다른 logic을 활용할 수 있을 것이다.)
    - 한편, 레벨 50을 종국에는 넘었지만 첫 세션에서 넘기지 않은 나머지 플레이어들을 non-binger로 분류했다.


## Part 4. Binger vs. Non-Binger 비교

### 04_rainbow_plot.R
- x축을 레벨 1~50으로, 각 플레이어가 레벨별로 어떤 플레이 패턴을 보였는지 시각화한다.
- 특히 binger와 non-binger 간의 플레이 패턴에 어떤 차이가 있는지 살펴보고자 했다.