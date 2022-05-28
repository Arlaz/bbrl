# BBRL #

`bbrl`- A Flexible and Simple Library for Reinforcement Learning inspired from SaLinA

BBRL stands for "BlackBoard Reinforcement Learning". Initially, [the BBRL library](https://github.com/osigaud/bbrl) was a fork of [the SaLinA library](https://github.com/facebookresearch/salina). 
But SaLinA is a general model for sequential learning whereas BBRL is dedicated to RL, thus it focuses on a subset of SaLinA. 
Morevover, BBRL is designed for education purpose (in particular, to teach various RL algorithms, concepts and phenomena). 
Thus the fork slowly drifted away from SaLinA and became independent after a few months, even if some parts of the code are still inherited from SaLinA.

**Documentation**:[Read the docs](https://bbrl.readthedocs.io/en/latest/)

## TL;DR.

`bbrl` is a lightweight library extending PyTorch modules for developping **Reinforcement Learning** models
* It supports simultaneously training with AutoReset on multiple environments
* It works on multiple CPUs and GPUs

# Citing `bbrl`

BBRL being inspired from SaLinA, please use this bibtex if you want to cite BBRL in your publications:

Link to the paper: [SaLinA: Sequential Learning of Agents](https://arxiv.org/abs/2110.07910)

```
    @misc{salina,
        author = {Ludovic Denoyer, Alfredo de la Fuente, Song Duong, Jean-Baptiste Gaya, Pierre-Alexandre Kamienny, Daniel H. Thompson},
        title = {SaLinA: Sequential Learning of Agents},
        year = {2021},
        publisher = {Arxiv},
        howpublished = {\url{https://gitHub.com/facebookresearch/salina}},
    }

```

## News

* May 2022:
* * First commit of the BBRL repository

* March 2022:
* * Forked SaLinA and strated to modify the model

## Quick Start

* Just clone the repo
* `pip install -e .`

### Learning RL with `bbrl`

Will come soon

### Documentation

Will come soon

**For development, see [contributing](CONTRIBUTING.md)**

## Dependencies

`bbrl` utilizes `pytorch`, `hydra` for configuring experiments, and `gym` for reinforcement learning algorithms.

## Note on the logger

We provide a simple Logger that logs in both tensorboard format, but also as pickle files that can be re-read to make tables and figures. See [logger](salina/logger.py). This logger can be easily replaced by any other logger.

## License

`bbrl` is released under the MIT license. See [LICENSE](LICENSE) for additional details about it.
