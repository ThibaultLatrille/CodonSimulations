#!/usr/bin/env bash
EXPERIMENT=./Experiments/Simulations
SUBSET=${EXPERIMENT}Subset
rm -rf ${SUBSET}
mkdir ${SUBSET}
cp ${EXPERIMENT}/*.fasta ${SUBSET}
cp ${EXPERIMENT}/*.ali ${SUBSET}
cp ${EXPERIMENT}/*.nhx ${SUBSET}
cp ${EXPERIMENT}/*.dnds.tsv ${SUBSET}
cp ${EXPERIMENT}/config.yaml ${SUBSET}
