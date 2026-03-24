# Can I Guess Your Next Word?

A next-word prediction app where you type one word at a time and a neural network tries to guess what comes next. The model learns from your input as you go. The more you type, the better it gets at predicting you.

No TensorFlow. No PyTorch. Just numpy and an LSTM built from scratch.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red)
![NumPy](https://img.shields.io/badge/NumPy-LSTM-orange)

## Try it

👉 **[can-i-guess-your-next-word.streamlit.app](https://can-i-guess-your-next-word.streamlit.app/)**

<!-- Add a screenshot or GIF here if you have one -->
<!-- ![demo](assets/demo.gif) -->

---

## How it works

When you first open the app, the model trains on a built-in English text corpus. This takes about 15-30 seconds. Once that's done, you start typing.

Your first word gives the model context. It doesn't try to predict this one since it has nothing to go on yet. From the second word onward, the model shows its top 5 guesses with probability bars. You type your word, and it tells you whether it got it right, came close (in the top 10 but not top 5), or missed entirely.

After every word you type, the model runs a few rounds of fine-tuning on your recent input. This is online learning: the model's weights are being updated in real time based on what you're writing. It's not just memorising your words. It's adjusting the internal parameters of the network so that your patterns influence future predictions.

### The three buttons

| Button | What it does |
|---|---|
| **New sentence** | Archives your current sentence into memory, clears the text area so you can start fresh. Your stats (accuracy, word count) and everything the model has learned are kept. |
| **Retrain with my words** | Takes all the sentences you've typed (current + archived), merges them into the training corpus, and retrains the entire model from scratch. Your writing patterns get baked into the base model instead of just being fine-tuned on top. Unlocks after 5 words. |
| **Full reset** | Wipes everything: stats, history, learned patterns, model weights. Starts completely from zero. |

---

## The model

This is a single-layer LSTM (Long Short-Term Memory) network. Here's what each part does:

### Embedding layer
Each word in the vocabulary gets mapped to a 48-dimensional dense vector. These vectors are learned during training. Words that appear in similar contexts end up with similar vectors. This is the same idea behind Word2Vec, just learned jointly with the rest of the network.

### LSTM cell
The core of the model. An LSTM maintains two internal states: a hidden state `h` and a cell state `c`. At each time step, it takes the current word embedding and the previous hidden state, and passes them through four gates:

- **Forget gate**: decides what information from the previous cell state to throw away
- **Input gate**: decides what new information to store
- **Cell gate**: creates candidate values to add to the cell state
- **Output gate**: decides what part of the cell state to output as the hidden state

This gating mechanism is what lets LSTMs handle sequences. A regular neural network has no memory of previous inputs. An LSTM explicitly learns what to remember and what to forget, which is why it works for language. The meaning of a word often depends on words that came several steps earlier.

The hidden dimension is 64 units.

### Output layer
The final hidden state goes through a dense layer with softmax activation, producing a probability distribution over the entire vocabulary. The top 5 probabilities are what you see in the app.

### Training
- Backpropagation through time (BPTT): gradients flow backward through the sequence
- Stochastic gradient descent with learning rate decay (starts at 0.02, decays by 0.85x per epoch)
- Gradient clipping at +/-5 to prevent exploding gradients
- 8 epochs over the corpus with sequence length of 8 tokens

### Online learning (fine-tuning)
After each word you type, the model runs 5 passes of gradient descent on your last 12 words with a learning rate of 0.008. New words you type that aren't in the vocabulary get added dynamically. The embedding matrix and output layer expand to accommodate them.

---

## Features

- Top 5 predictions with probability bars
- Near-miss detection: tells you when your word was in the top 10 but not top 5
- Session persistence: refresh the page and your history is restored
- "Patterns I've learned" section showing word pairs (bigrams) the model has picked up from you
- Past sentence memory: archived sentences are displayed so you can see what the model has been trained on
- Custom corpus upload: drag in any `.txt` file to retrain the base model on different text
- Accuracy tracking across your entire session

---

## Run it locally

```bash
git clone https://github.com/ayjzhuang/next-word-prediction.git
cd next-word-prediction
pip install -r requirements.txt
streamlit run app.py
```

Opens at `http://localhost:8501`.

## Project structure

```
next-word-prediction/
├── app.py              # model, training, UI, all in one file
├── requirements.txt    # streamlit + numpy
├── .gitignore
└── README.md
```

## Dependencies

Just two:
- `streamlit` for the web interface
- `numpy` for the entire LSTM implementation

Everything else is Python standard library (`re`, `json`, `os`, `random`, `collections`).

---

## Deploy to Streamlit Community Cloud

1. Push your code to a GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click "New app", select your repo, branch `main`, main file `app.py`
4. Click Deploy. You'll get a public URL in about a minute.

---

## 简单说明

这个项目是一个"猜你下一个词"的小应用。你一个词一个词地打字，模型会试着猜你接下来要打什么。

核心是一个用 numpy 手写的 LSTM 神经网络。没有用 TensorFlow 或 PyTorch，所有的矩阵运算、反向传播、梯度更新都是自己写的。

模型先在一段英文语料上训练，学会基本的语言规律（比如 "it was the" 后面大概率跟 "best" 或 "worst"）。然后在你打字的过程中，模型会用你最近输入的词做实时微调，慢慢适应你的用词习惯。

三个按钮的作用：
- **New sentence**: 存档当前句子，开始新的一轮，模型记忆和统计数据都保留
- **Retrain with my words**: 把你打过的所有句子混进训练语料，重新从头训练整个模型，让你的用词习惯真正融入模型
- **Full reset**: 全部清零，从头开始

运行方法：装好 Python，然后 `pip install streamlit numpy`，再 `streamlit run app.py` 就行。

或者直接访问在线版：[can-i-guess-your-next-word.streamlit.app](https://can-i-guess-your-next-word.streamlit.app/)
