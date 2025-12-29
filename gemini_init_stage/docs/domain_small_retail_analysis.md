# **도메인 분석: 소규모 리테일 및 쇼핑몰 재고 모니터링**

소형 리테일(편의점, 소규모 마트, 무인 점포) 환경에 특화된 분석 데이터 및 시나리오입니다.

## **1. 도메인 핵심 지표 (KPI)**

- **OSA (On-Shelf Availability):** 고객이 찾는 시점에 물건이 진열대에 있을 확률.
- **OOS (Out-of-Stock) Rate:** 품절로 인해 판매 기회를 상실한 비율.
- **MTTR (Mean Time To Replenish):** 품절 감지 후 재진열까지 걸리는 평균 시간.

## **2. 초기 키워드 데이터 세트 (30개)**

### **2.1 시장 수요 및 문제 (10)**

on-shelf availability, retail stockout, 품절 방지 시스템, 매대 빈자리 감지, shelf gap detection, retail replenishment, OOS rate retail, 점포 재고 관리, 진열 가용성, lost sales stockout.

### **2.2 운영 고통 및 워크플로우 (10)**

manual inventory count, 편의점 재고 조사, phantom stock, inventory accuracy retail, cycle counting retail, 재고 불일치, 유통기한 관리 자동화, 매대 보충 지연, 점포 운영 비효율, shrinkage inventory.

### **2.3 솔루션 및 기술 탐색 (10)**

shelf monitoring camera, computer vision retail, AI shelf analytics, 스마트 선반 카메라, CCTV 재고 분석, edge AI camera monitoring, product facing detection, real-time shelf monitoring, 매대 품절 알림, 무인 점포 재고 시스템.

## **3. 사용자 시나리오 (User Story)**

1. **감지:** 카메라가 삼각김밥 매대의 '공백'을 포착합니다.
2. **판단:** 서버에서 현재 시간이 피크 타임임을 감안하여 '긴급 보충' 필요로 판단합니다.
3. **알림:** 점주의 스마트폰으로 "A구역 삼각김밥 품절 발생, 즉시 보충 필요" 알림이 발송됩니다.
4. **조치:** 점주가 대시보드에서 실시간 이미지를 확인하고 창고에서 물건을 가져와 진열합니다.
5. **완료:** 카메라가 다시 물체가 있음을 확인하고 로그를 자동 생성합니다.