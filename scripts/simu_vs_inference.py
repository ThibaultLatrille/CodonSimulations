#!python3
import os
from os.path import basename
import numpy as np
import pandas as pd
from glob import glob
from ete3 import Tree
import statsmodels.api as sm
from plot_module import *

if __name__ == '__main__':
    plt.figure(figsize=(1920 / my_dpi, 1080 / my_dpi), dpi=my_dpi)
    simu_path = "Experiments/SimulationsSubset"
    dico_r2 = {"Experiment": []}

    for filepath in sorted(glob("{0}/*.nhx".format(simu_path))):
        simu = basename(filepath).replace(".nhx", "")
        dico_r2["Experiment"].append(simu)

        for model in ["MG94", "YN98"]:
            if model not in dico_r2: dico_r2[model] = []
            biopp_counts = "DataBiopp/counts_" + model
            plot_dir = biopp_counts + "/plots"
            os.makedirs(plot_dir, exist_ok=True)

            exp = biopp_counts + "/" + simu
            dN_tree = Tree(exp + ".counts_dN.dnd", format=1)
            dS_tree = Tree(exp + ".counts_dS.dnd", format=1)
            simu_tree = Tree(filepath, format=1)

            node_dico = {"estimation": []}
            for n_sim, n_dN, n_dS in zip(simu_tree.iter_descendants(), dN_tree.iter_descendants(),
                                         dS_tree.iter_descendants()):
                assert (set(n_dN.get_leaf_names()) == set(n_dS.get_leaf_names()))
                assert (set(n_sim.get_leaf_names()) == set(n_dN.get_leaf_names()))
                if n_sim.is_root(): continue
                node_dico["estimation"].append(n_dN.dist / n_dS.dist)
                for attr in n_sim.features:
                    if not (("dNdS_count" in attr) or ("Branch_population_size" in attr)): continue
                    if attr not in node_dico: node_dico[attr] = []
                    node_dico[attr].append(float(getattr(n_sim, attr)))

            y = node_dico["estimation"]
            for param, x in node_dico.items():
                if param == "estimation": continue

                plt.scatter(x, y, linewidth=2, color="#5D80B4")

                if "population_size" in param:
                    results = sm.OLS(y, sm.add_constant(np.log(x))).fit()
                    b, a = results.params[0:2]
                    idf = np.logspace(np.log(min(x)), np.log(max(x)), 30, base=np.exp(1))
                    linear = a * np.log(idf) + b
                    plt.xscale("log")
                else:
                    results = sm.OLS(y, sm.add_constant(x)).fit()
                    b, a = results.params[0:2]
                    idf = np.linspace(min(x), max(x), 30)
                    linear = a * idf + b
                    plt.xscale("linear")
                    dico_r2[model].append(results.rsquared)

                plt.plot(idf, linear, '-', linewidth=4, linestyle="--", label='$r^2$={0:.2g}'.format(results.rsquared))
                plt.xlabel("Simulated " + ("dN/dS" if "dNdS" in param else "effective population size"),
                           fontsize=legend_size)
                plt.ylabel("Inferred dN/dS (Bio++ {0})".format(model), fontsize=legend_size)
                plt.legend(fontsize=legend_size)

                plt.tight_layout()
                plt.savefig("{0}/{1}.{2}.pdf".format(plot_dir, basename(exp), param), format="pdf", dpi=my_dpi)
                plt.savefig("{0}/{1}.{2}.png".format(plot_dir, basename(exp), param), format="png", dpi=my_dpi)
                plt.clf()
        plt.close('all')

    pd.DataFrame(dico_r2).to_csv("DataBiopp/results.tsv", sep="\t", index=False)
