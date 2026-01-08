#!/bin/bash
# 결과와 함께 'SKILL_EXECUTED'라는 표식을 남깁니다.
RESULT=$(($1 $2 $3))
echo "[SKILL_LOG] 연산 수행: $1 $2 $3 = $RESULT" >> .gemini/skills/expert_calc/history.log
echo "최종 결과: $RESULT (Skill Engine 사용됨)"
