#!/usr/bin/env bash
for EXPERIMENT in ./Experiments/root*/; do
  SUBSET=DataSimulated/$(basename "${EXPERIMENT}")
  rm -rf "${SUBSET}"
  mkdir "${SUBSET}"
  cp "${EXPERIMENT}"/*.fasta "${SUBSET}"
  cp "${EXPERIMENT}"/*.ali "${SUBSET}"
  cp "${EXPERIMENT}"/*.nhx "${SUBSET}"
  cp "${EXPERIMENT}"/*.tree "${SUBSET}"
  cp "${EXPERIMENT}"/*.dnds.tsv "${SUBSET}"
  cp "${EXPERIMENT}"/config.yaml "${SUBSET}"
done
