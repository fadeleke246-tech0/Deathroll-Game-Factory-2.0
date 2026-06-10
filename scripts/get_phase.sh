#!/bin/bash
PHASE=1
if [ -f data/run_state.json ]; then
    PHASE=$(python -c "import json; f=open('data/run_state.json'); d=json.load(f); print(d.get('phase',1))")
fi
echo "phase=$PHASE"
