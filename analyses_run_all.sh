#!/usr/bin/env bash
CPU=2
for EXPERIMENT in Experiments/*.yaml; do
  python3 ./scripts/simulated_experiment.py -f ${FOLDER} -c $(basename "${EXPERIMENT}") -j ${CPU}
done
