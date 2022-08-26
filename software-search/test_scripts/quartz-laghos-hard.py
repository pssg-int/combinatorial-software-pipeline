#!/usr/bin/env spack-python
from argparse import ArgumentParser
import os, sys
sys.path.append('/usr/workspace/synk1/combinatorial-software-pipeline/software-search/')
from software_search.software import Software
from software_search.software_search import search
from software_search.grid_search import GridSearch
from software_search.random_search import RandomSearch
from software_search.compiler import Compiler
from software_search.runner import BashRunner


def get_args():
    parser = ArgumentParser()
    parser.add_argument('-d', '--dry', action='store_true', help='Dry run.')
    parser.add_argument('-e', '--spack-env', type=str, help='Spack environment to install in.')
    parser.add_argument('-o', '--output-dir', type=str, default='/usr/workspace/synk1/quartz_laghos_output', help='Directory to log output files into')
    return parser.parse_args()


def main():
    args = get_args()
    print(sys.version)

    mpis = [
        Software('intel-mpi').make_range(versions=['2019.0','2019.8','2018.0','2017.1','5.1.3']),
        Software('mvapich2').make_range(versions=['2.2','2.3','2.3.6']),
        Software('openmpi').make_range(versions=['2.0.0','2.1.0','3.0.1','4.0.0'])
    ]

    compilers = [
	    Compiler('gcc', version='4.9.3'),
	    Compiler('intel', version='19.0.4.227')
    ]

    main_software = Software('laghos', version='3.1', run_cmd='laghos',
                            variants='', run_args='-p 1 -dim 2 -rs 4 -tf 0.6 -pa')

    search_strategy = GridSearch()
    runner = BashRunner(output_dir=args.output_dir)
    runner.set_mpi(num_ranks=32, run_cmd='srun')

    search(search_strategy, runner, main_software, compilers, 
        [mpis], dry=args.dry, spack_env=args.spack_env)


if __name__ == '__main__':
    main()
