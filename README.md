# Can I Guess Your Next Word?

An interactive next-word prediction app. You type one word at a time, and an LSTM neural network tries to predict what you'll type next. It learns from your input in real time.

Built with Streamlit and a pure-numpy LSTM - no TensorFlow or PyTorch required.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red)

## Try it live

👉 [**Launch the app on Streamlit**](https://can-i-guess-your-next-word.streamlit.app/)

## How it works

1. The model trains on a text corpus when you first load the page (~15-30s)
2. You type your first word - this gives the model context
3. From the second word onward, the model shows its top 5 predictions with probabilities
4. You type your actual word, and the model tells you if it guessed right, was close (top 10), or missed
5. After each word, the model fine-tunes on your recent input - so it adapts to your writing style
6. Your session is saved locally, so refreshing the page keeps your history and the model remembers your patterns

## What's under the hood

The model is a single-layer LSTM (Long Short-Term Memory) network implemented from scratch in numpy:

- Embedding layer (48 dimensions) converts words to dense vectors
- LSTM cell with forget, input, output gates (64 hidden units)
- Dense output layer with softmax over the full vocabulary
- Trained with backpropagation through time (BPTT) and SGD
- Gradient clipping to prevent exploding gradients
- Learning rate decay across epochs

Online learning: after each word you type, the model runs 5 passes of fine-tuning on your recent words. New words you type are added to the vocabulary dynamically.

## Features

- Top 5 predictions with probability bars after each word
- Near-miss detection (your word was in top 10 but not top 5)
- Session persistence - refresh the page and your history is restored
- "Patterns I've learned" section showing word pairs the model picked up from you
- Custom corpus upload - retrain the base model on any .txt file
- Accuracy tracking across your session

## Quick start

```bash
git clone https://github.com/ayjzhuang/next-word-prediction.git
cd next-word-prediction
pip install -r requirements.txt
streamlit run app.py
```

Opens at `http://localhost:8501`

## Project structure

```
next-word-prediction/
├── app.py              # everything - model, training, UI
├── requirements.txt    # streamlit + numpy
├── .gitignore
└── README.md
```

## Dependencies

- `streamlit` - web UI
- `numpy` - LSTM implementation

That's it. Everything else is Python standard library.

## Deploying to Streamlit Community Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select your repo, branch `main`, and file `app.py`
5. Click Deploy - it'll give you a public URL

---

## 简单说明

这是一个下一个词预测的小项目。你一个字一个字地打，模型会猜你接下来要打什么词。

核心是一个用 numpy 手写的 LSTM 神经网络，不依赖 TensorFlow 或 PyTorch。模型先在一段英文语料上训练，然后在你打字的过程中实时学习你的用词习惯。打得越多，它猜得越准。

每次你输入一个词，模型会：
- 给出它认为最可能的 5 个词和对应的概率
- 告诉你它猜对了、接近了、还是完全没猜到
- 用你最近打的词做几轮微调，慢慢适应你的风格

刷新页面不会丢失记录，模型会重新加载你之前打过的内容继续学习。

运行方式：装好 Python，然后 `pip install streamlit numpy`，再 `streamlit run app.py` 就行了。
