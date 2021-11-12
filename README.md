# Runtime domain adaptation
## Introduction
In this tutorial we will learn how to use Marian to translate texts using
on-the-fly domain adaptation to improve translation quality by adapting the NMT
model to the text at hand.

TODO

## Data preparation
First we need to prepare the data that we will be using to adapt the generic NMT
model to the domain of the document we want to translate. We will download the
data and the model, set up some tools and preprocess the data.

### Downloading the data and the NMT model
You should download and extract the data.
```sh
wget http://TODO.tar.gz
tar zxvf TODO.tar.gz
cd TODO
```

### Creating the anaconda environment
We will be using `virtualenv` to set up a virtual Python environment to host the
tools we will be using for data preprocessing. Virtualenv should be easily
available through your Linux distribution's package manager, e.g.,
```sh
# Ubuntu
sudo apt-get install virtualenv
# Arch Linux
sudo pacman -S python-virtualenv
```
but it should be already available on the shared server we're using for the tutorial.

Use the `virtualenv` command to create a local directory called `venv` (or any
other name you choose) for storing the Python tools. Then activate the virtual environment.
```sh
# create the virtual environment
virtualenv venv
# activate it
. ./venv/bin/activate
```

Now install some Python tools that we will be using
```sh
pip install sacrebleu TODO
```
