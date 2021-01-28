# Temporal Difference Learning

## Introduction
This repository consists of implementations of Temporal Difference (TD) Learning methods in the deep learning setting. Algorithms are implemented in [`PyTorch`](Pytorch/) on a range of problems. Custom toy problems are provided in the [`MDPs`](MDPs/) folder.

## TD Algorithms
Following are the TD algorithms implemented-

|Algorithm|Link|Implementation|Status|
|:-------:|:--:|:------------:|:---:|
|Sarsa|[Sutton & Barto](http://incompleteideas.net/book/RLbook2020.pdf)|[`sarsa.py`](Pytorch/sarsa.py)|Works well|
|Q-Learning|[Sutton & Barto](http://incompleteideas.net/book/RLbook2020.pdf)|[`qlearning.py`](Pytorch/qlearning.py)|:heavy_check_mark:|
|Expected Sarsa|[Sutton & Barto](http://incompleteideas.net/book/RLbook2020.pdf)|[`expectedsarsa.py`](Pytorch/expectedsarsa.py)|:heavy_check_mark:|
|Double Sarsa|[Sutton & Barto](http://incompleteideas.net/book/RLbook2020.pdf)|[`doublesarsa.py`](Pytorch/doublesarsa.py)|:heavy_check_mark:|
|Double Q-Learning|[Sutton & Barto](http://incompleteideas.net/book/RLbook2020.pdf)|[`doubleqlearning.py`](Pytorch/doubleqlearning.py)|:heavy_check_mark:|
|Double Expected Sarsa|[Sutton & Barto](http://incompleteideas.net/book/RLbook2020.pdf)|[`doubleexpectedsarsa.py`](Pytorch/doubleexpectedsarsa.py)|:heavy_check_mark:|


## Custom Environments
Following is the list of custom toy environments-

|Environment Name|Link|Implementation|
|:--------------:|:--:|:------------:|
|Cyclic MDP|[ESAC](https://arxiv.org/pdf/2007.13690.pdf)|[link](MDPs/cyclic_mdp.py)|
|One-state MDP|[Sutton & Barto](http://incompleteideas.net/book/RLbook2020.pdf)|[link](MDPs/one_state_mdp.py)|
|One-state Gaussian MDP|[Sutton & Barto](http://incompleteideas.net/book/RLbook2020.pdf)|[link](MDPs/one_state_gaussian_mdp.py)|

## Usage

To run an implementation, use the following command- 
```
python main.py --alg <ALGORITHM> --env <ENV> --num_steps <STEPS>
```

For example, to run Q-Learning on the CartPole-v0 environment for 10000 steps, use the following-
```
python main.py --alg QLearning --env CartPole-v0 --num_steps 10000
``` 

To view the full list of arguments run the following-
```
python main.py --help
```
## Citation
If you find these implementations helpful then please cite the following-
```
@misc{karush17tdlearning,
  author = {Karush Suri},
  title = {Temporal Difference Learning},
  year = {2021},
  howpublished = {\url{https://github.com/karush17/Temporal-Difference-Learning}},
  note = {commit xxxxxxx}
}
```


