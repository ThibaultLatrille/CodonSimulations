#!python3
import argparse
import os
from subprocess import run


def create_experiment(name, config, screen, sbatch, nbr_cpu):
    os.chdir("Experiments")
    if name.strip() == "": name = config.replace(".yaml", "")
    exp_path = os.getcwd() + '/' + name
    os.makedirs(exp_path, exist_ok=True)
    os.system('cp {0} {1}/config.yaml'.format(config, exp_path))
    os.remove(exp_path + "/Snakefile") if os.path.exists(exp_path + "/Snakefile") else None
    os.symlink(os.getcwd() + "/Snakefile", exp_path + "/Snakefile")
    run_file = exp_path + "/snakeslurm.sh"
    with open(run_file, 'w') as w:
        w.write("#!/usr/bin/env bash\n")
        run_str = 'snakemake '
        if sbatch:
            run_str += '-j 99 --cluster "sbatch -J {0} -p long -N 1 ' \
                       '-o {1}/slurm.%x.%j.out -e {1}/slurm.%x.%j.err '.format(name, exp_path)
            run_str += '--cpus-per-task={params.threads} --mem={params.mem} -t {params.time}"\n'
        else:
            run_str += "-j {0} --printshellcmds".format(nbr_cpu)
        w.write(run_str)
    os.system("chmod 755 " + run_file)
    cmd = 'cd ' + exp_path + ' && ./snakeslurm.sh'
    screen_cmd = 'screen -dmS ' + name + ' bash -c "' + cmd + '"'
    with open(exp_path + "/screen.sh", 'w') as w:
        w.write("#!/usr/bin/env bash\n")
        w.write(screen_cmd)
    if screen:
        print(screen_cmd)
        run(screen_cmd, shell=True)
    else:
        print(cmd)
        run(cmd, shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-n', '--name', required=False, type=str, default="", dest="name")
    parser.add_argument('-c', '--config', required=True, type=str, default="config.yaml", dest="config")
    parser.add_argument('-s', '--screen', required=False, type=bool, default=False, dest="screen")
    parser.add_argument('-b', '--sbatch', required=False, type=bool, default=False, dest="sbatch")
    parser.add_argument('-j', '--nbr_cpu', required=False, type=int, default=6, dest="nbr_cpu")
    args = parser.parse_args()
    create_experiment(args.name, args.config, args.screen, args.sbatch, args.nbr_cpu)
