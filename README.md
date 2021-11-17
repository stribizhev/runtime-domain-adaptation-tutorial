# Runtime domain adaptation
## Introduction
In this tutorial we will learn how to use Marian to translate texts using
on-the-fly domain adaptation to improve translation quality by adapting the NMT
model to the text at hand.

TODO

## Software dependencies
We will be using multiple different tools to preprocess the data and measure the
translation quality at the end. These tools must be installed before we begin.

### Pre-installed tools
These tools should already be available on the shared server we're using for the
tutorial. You should install these only if you're following the tutorial using
your own computer. These tools should be easily available through your Linux
distribution's package manager. The setup instructions will target Ubuntu using
the `apt` packaging tool. If you're not using Linux, please search for setup
instructions online.

We will need Python 3 (we've used Python 3.6.9 when testing the instructions in
the tutorial) and Perl to run data processing scripts, Virtualenv to allow
installing Python packages locally without root permissions (instead of
system-wide).
```sh
# Update the package list
sudo apt-get update
# Install the software
sudo apt-get install python3 perl virtualenv
```

### Install Python tools in a virtual environment
Use the `virtualenv` command to create a local directory called `venv` (or any
other name you choose) for storing the Python tools. Then activate the virtual environment.
```sh
# Create the virtual environment
virtualenv venv --python=/usr/bin/python3
# Activate it
. ./venv/bin/activate
```

Now install some Python tools that we will be using
```sh
pip install sacrebleu bpe requests TODO
```

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

### Preprocessing the data
Preprocessing the data involves:
1. punctuation normalization,
2. tokenization,
3. truecasing,
4. byte-pair encoding.

These steps are needed to convert the text into a form that's expected by the
NMT model.

#### Set some variables
These will be used down below.
```sh
# TODO
prefix=$1
src=$2
trg=$3
prefix_dev=$4
```

#### Punctuation normalization
Punctuation normalization attempts to reduce the variability of punctuation use
in text by converting classes of similar punctuation into a single normal form.
E.g., multiple spaces are converted to a single space, quote characters like «,
'', „ are converted to ", etc.

Apply `normalize-punctuation.perl` from Moses scripts to the source and target
side of the parallel corpus.

```sh
# Process source
cat ${prefix}.${src} \
  | ~/software/mosesdecoder/scripts/tokenizer/normalize-punctuation.perl \
  > ${prefix}.norm.${src}

# Process target
cat ${prefix}.${trg} \
  | ~/software/mosesdecoder/scripts/tokenizer/normalize-punctuation.perl \
  > ${prefix}.norm.${trg}
```

#### Tokenization
Tokenization separates TODO 

```sh
# Process source
cat ${prefix}.norm.${src} \
  | ~/software/mosesdecoder/scripts/tokenizer/tokenizer.perl -l ${src} -no-escape -threads 1 \
  > ${prefix}.tok.${src}

# Process target
cat ${prefix}.norm.${trg} \
  | ~/software/mosesdecoder/scripts/tokenizer/tokenizer.perl -l ${trg} -no-escape -threads 1 \
  > ${prefix}.tok.${trg}
```

#### Truecasing
Truecasing converts word casing into a standard form regardless of its place in
the sentence. E.g., common nouns that appear at the start of the sentence get
lowercased, proper nouns get uppercased.

Truecasing uses a pre-trained truecasing model that must match the one that was
used when training the system.

```sh
# Process source
~/software/mosesdecoder/scripts/recaser/truecase.perl \
  --model trucase.${src} -a \
  < ${prefix}.tok.${src} \
  > ${prefix}.tc.${src}

# Process target
~/software/mosesdecoder/scripts/recaser/truecase.perl \
  --model trucase.${trg} -a \
  < ${prefix}.tok.${trg} \
  > ${prefix}.tc.${trg}
```

#### Apply BPE
Byte-pair encoding (BPE) breaks down words into subword units -- a set of common
parts shared among all words. E.g.,
> equipment and materials are necessary but not supplied
turns into
> equipment and materi@@ als are n@@ ec@@ es@@ sary but not suppl@@ ied

```sh
# Process source
$TODO_BPE_DIR/apply_bpe.py -c ${src}${trg}.bpe < ${prefix_dev}.tc.${src} > ${prefix_dev}.bpe.${src}
# Process target
$TODO_BPE_DIR/apply_bpe.py -c ${src}${trg}.bpe < ${prefix_dev}.tc.${trg} > ${prefix_dev}.bpe.${trg}
```


## Translation
To evaluate the effectiveness of runtime-domain adaptation, we will compare how
it performs relative to regular translation. To do so, we will simulate a human
translator who's translating a document by post-editing an NMT system's outputs.
In scenario a) the *translator* will be continuously submitting the post-edited
sentences to supply the NMT system with examples to use to adapt to the domain
of the document. In scenario b) run-time domain adaptation will not be used.

### Runtime domain adaptation (scenario a)
Run the `client.py` script by supplying it with an url to the runtime domain
adaptation webservice, your unique ID and source and target files.

```sh
./client.py --uid $UID \
  --source ./TODO/source --target ./TODO/target \
  http://localhost:$PORT \
  > output.dynamic.$trg
```

### Regular translation (scenario b)
To translate without using runtime domain adaptation, simply use the same
command as previously without supplying the `--target` option.

```sh
./client.py --uid $UID \
  --source ./TODO/source \
  http://localhost:$PORT \
  > output.regular.$trg
```

### Calculating results
Calculate BLEU for both outputs to compare the quality of translations.

```sh
# Calculate BLEU for the translations that used runtime domain adaptation
sacrebleu output.dynamic.$trg < ./TODO/target | tee dynamic.bleu

# Calculate BLEU for the translations that didn't use runtime domain adaptation
sacrebleu output.regular.$trg < ./TODO/target | tee regular.bleu
```
