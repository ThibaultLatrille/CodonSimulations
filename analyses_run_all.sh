#!/usr/bin/env bash
for CONFIG in ./Experiments/*.yaml; do
  python3 ./scripts/simulated_experiment.py --config $(basename "${CONFIG}") -j 4
done