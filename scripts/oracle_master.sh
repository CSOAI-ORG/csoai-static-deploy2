#!/bin/bash
# SOV8 ORACLE ORCHESTRATOR — All 8 TUIs managed from Oracle
# No more MacBook. All work runs from here.
# Usage: bash oracle_master.sh [start|status|sync|kaggle|eat]

set -e
WORK="/home/ubuntu/sov-work"
LOGS="$WORK/logs"
mkdir -p "$LOGS"

case "${1:-status}" in

start)
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║  SOV8 ORACLE ORCHESTRATOR — Starting All TUIs          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    
    # T1: Kaggle training monitor
    echo "[T1] Kaggle training monitor..."
    nohup python3 $WORK/scripts/kaggle_monitor.py > $LOGS/t1_kaggle.log 2>&1 &
    echo "  PID: $!"
    
    # T2: EAT cycle runner
    echo "[T2] EAT cycle runner..."
    nohup python3 $WORK/sov7_synthesis_orchestrator.py --mode auto --cycles 10 > $LOGS/t2_eat.log 2>&1 &
    echo "  PID: $!"
    
    # T3: Groq distillation
    echo "[T3] Groq distillation..."
    nohup python3 $WORK/sov7_synthesis/groq_distill_200.py > $LOGS/t3_groq.log 2>&1 &
    echo "  PID: $!"
    
    # T4: Benchmark suite
    echo "[T4] Benchmark suite..."
    nohup python3 $WORK/sov7_synthesis/benchmark_all.py > $LOGS/t4_bench.log 2>&1 &
    echo "  PID: $!"
    
    # T5: Visual synthesis
    echo "[T5] Visual synthesis..."
    nohup python3 $WORK/sov7_visual_synthesis.py > $LOGS/t5_visual.log 2>&1 &
    echo "  PID: $!"
    
    # T6: ASI evolve
    echo "[T6] ASI evolve..."
    nohup python3 $WORK/asi_evolve_overnight.py > $LOGS/t6_asi.log 2>&1 &
    echo "  PID: $!"
    
    # T7: Monitoring
    echo "[T7] Monitoring..."
    nohup bash $WORK/scripts/monitor_all.sh > $LOGS/t7_monitor.log 2>&1 &
    echo "  PID: $!"
    
    # T8: Science loop
    echo "[T8] Science loop..."
    nohup python3 $WORK/sov7_science_loop.py cycle --cycles 5 > $LOGS/t8_science.log 2>&1 &
    echo "  PID: $!"
    
    echo ""
    echo "All 8 TUIs started. Logs: $LOGS/"
    echo "Monitor: bash oracle_master.sh status"
    ;;

status)
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║  SOV8 ORACLE STATUS                                    ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo ""
    echo "=== DISK ==="
    df -h / | tail -1
    echo ""
    echo "=== MEMORY ==="
    free -h | head -2
    echo ""
    echo "=== RUNNING PYTHON ==="
    ps aux | grep python3 | grep -v grep | wc -l
    echo " processes"
    echo ""
    echo "=== LOGS ==="
    ls -lh $LOGS/ 2>/dev/null | tail -10
    echo ""
    echo "=== KAGGLE STATUS ==="
    kaggle kernels list --user nicktempleman --sort-by dateRun 2>/dev/null | head -5
    echo ""
    echo "=== LATEST EAT RESULTS ==="
    ls -lt $WORK/sov7_synthesis/eat_*.json 2>/dev/null | head -3
    echo ""
    echo "=== ARTIFACTS ==="
    du -sh $WORK/sov7_synthesis/ 2>/dev/null
    du -sh $WORK/benchmark-results/ 2>/dev/null
    du -sh $WORK/eat_results/ 2>/dev/null
    du -sh $WORK/honey/ 2>/dev/null
    ;;

sync)
    echo "Syncing from MacBook..."
    rsync -avz -e "ssh -i ~/.ssh/id_ed25519" \
      /Users/nicholas/clawd/csoai-static-deploy2/ \
      ubuntu@145.241.232.16:/home/ubuntu/sov-work/ 2>&1 | tail -5
    echo "Sync complete."
    ;;

kaggle)
    echo "Pushing Kaggle notebooks..."
    for nb in $WORK/kaggle/*.py; do
        echo "  Pushing: $(basename $nb)"
        cd $(dirname $nb) && kaggle kernels push -p . 2>&1 | tail -1
    done
    ;;

eat)
    echo "Running EAT cycle..."
    python3 $WORK/sov7_synthesis_orchestrator.py --mode auto --cycles 3 2>&1
    ;;

*)
    echo "Usage: bash oracle_master.sh [start|status|sync|kaggle|eat]"
    ;;
esac
