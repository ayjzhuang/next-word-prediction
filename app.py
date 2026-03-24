import streamlit as st
import numpy as np
import re
import random
from collections import Counter

# ═══════════════════════════════════════════════
#  CONFIG
# ═══════════════════════════════════════════════

st.set_page_config(
    page_title="Can I Guess Your Next Word?",
    page_icon="⬡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    :root {
        --bg: #fafafa; --surface: #ffffff; --border: #e5e7eb;
        --text: #111827; --text2: #6b7280; --muted: #9ca3af;
        --accent: #2563eb; --accent-light: #eff6ff;
        --green: #059669; --green-bg: #f0fdf4;
        --red: #dc2626; --red-bg: #fef2f2;
    }
    .main, .stApp { background-color: var(--bg); }
    section[data-testid="stSidebar"] {
        background-color: var(--surface); border-right: 1px solid var(--border);
    }
    .app-header {
        font-family: 'Inter', sans-serif; font-size: 1.5rem; font-weight: 700;
        color: var(--text); margin-bottom: 2px;
    }
    .app-tag {
        display: inline-block; background: var(--accent-light); color: var(--accent);
        font-size: 0.65rem; font-weight: 600; padding: 2px 8px; border-radius: 4px;
        letter-spacing: 0.5px; margin-left: 6px; vertical-align: middle;
    }
    .app-sub {
        font-family: 'Inter', sans-serif; font-size: 0.85rem;
        color: var(--text2); margin-bottom: 1.2rem;
    }
    .metric-row { display: flex; gap: 10px; margin-bottom: 14px; }
    .metric-box {
        flex: 1; background: var(--surface); border: 1px solid var(--border);
        border-radius: 8px; padding: 12px 14px; text-align: center;
    }
    .metric-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.2rem; font-weight: 600; color: var(--text);
    }
    .metric-label {
        font-family: 'Inter', sans-serif; font-size: 0.65rem; color: var(--muted);
        text-transform: uppercase; letter-spacing: 0.6px; margin-top: 2px;
    }
    .card {
        background: var(--surface); border: 1px solid var(--border);
        border-radius: 8px; padding: 18px 22px; margin: 10px 0;
    }
    .pred-row {
        display: flex; align-items: center; gap: 12px;
        padding: 8px 0; border-bottom: 1px solid #f3f4f6;
    }
    .pred-row:last-child { border-bottom: none; }
    .pred-rank {
        font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;
        color: var(--muted); width: 18px; text-align: right;
    }
    .pred-word {
        font-family: 'JetBrains Mono', monospace; font-size: 0.95rem;
        font-weight: 600; color: var(--text); min-width: 100px;
    }
    .pred-bar-bg {
        flex: 1; background: #f3f4f6; border-radius: 4px;
        height: 6px; overflow: hidden;
    }
    .pred-bar-fill { height: 6px; border-radius: 4px; background: var(--accent); }
    .pred-pct {
        font-family: 'JetBrains Mono', monospace; font-size: 0.75rem;
        color: var(--text2); min-width: 45px; text-align: right;
    }
    .history-word {
        display: inline-block; padding: 2px 6px; margin: 1px 2px;
        border-radius: 4px; font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
    }
    .history-hit { background: #f0fdf4; color: #059669; }
    .history-miss { background: #f9fafb; color: #374151; }
    .stButton > button {
        background: var(--accent) !important; color: white !important;
        border: none !important; border-radius: 6px !important;
        padding: 6px 16px !important; font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important; font-size: 0.85rem !important;
    }
    .stButton > button:hover { background: #1d4ed8 !important; }
    .stTextInput input {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1rem !important; border-radius: 8px !important;
        border: 2px solid var(--border) !important; padding: 10px 14px !important;
    }
    .stTextInput input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
    }
    .train-info {
        font-family: 'JetBrains Mono', monospace; font-size: 0.78rem;
        color: var(--text2); background: #f9fafb; border: 1px solid var(--border);
        border-radius: 6px; padding: 10px 14px; margin: 6px 0;
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
#  CORPUS
# ═══════════════════════════════════════════════

DEFAULT_CORPUS = """
It was the best of times it was the worst of times it was the age of wisdom
it was the age of foolishness it was the epoch of belief it was the epoch of
incredulity it was the season of light it was the season of darkness it was
the spring of hope it was the winter of despair we had everything before us
we had nothing before us we were all going direct to heaven we were all going
direct the other way in short the period was so far like the present period
that some of its noisiest authorities insisted on its being received for good
or for evil in the superlative degree of comparison only there were a king with
a large jaw and a queen with a plain face on the throne of england there were
a king with a large jaw and a queen with a fair face on the throne of france
in both countries it was clearer than crystal to the lords of the state preserves

To be or not to be that is the question whether tis nobler in the mind to
suffer the slings and arrows of outrageous fortune or to take arms against a
sea of troubles and by opposing end them to die to sleep no more and by a
sleep to say we end the heartache and the thousand natural shocks that flesh
is heir to tis a consummation devoutly to be wished to die to sleep to sleep
perchance to dream ay there is the rub for in that sleep of death what dreams
may come when we have shuffled off this mortal coil must give us pause
there is the respect that makes calamity of so long life for who would bear
the whips and scorns of time the oppressor wrong the proud man contumely
the pangs of despised love the law delay the insolence of office and the spurns
that patient merit of the unworthy takes when he himself might his quietus make

It is a truth universally acknowledged that a single man in possession of a
good fortune must be in want of a wife however little known the feelings or
views of such a man may be on his first entering a neighbourhood this truth
is so well fixed in the minds of the surrounding families that he is considered
as the rightful property of some one or other of their daughters my dear mr
bennet said his lady to him one day have you heard that netherfield park is let
at last and it is a truth universally acknowledged do you not want to know who
has taken it asked his wife impatiently why my dear you must know that mrs long
has been here already and she told me all about it bennet made no answer

Call me ishmael some years ago never mind how long precisely having little
money in my purse and nothing particular to interest me on shore i thought i
would sail about a little and see the watery part of the world it is a way i
have of driving off the spleen and regulating the circulation whenever i find
myself growing grim about the mouth whenever it is a damp drizzly november in
my soul whenever i find myself involuntarily pausing before coffin warehouses
and bringing up the rear of every funeral i meet and especially whenever my
hypos get such an upper hand of me that it requires a strong moral principle
to prevent me from deliberately stepping into the street and methodically
knocking people hats off then i account it high time to get to sea as soon

In the beginning was the word and the word was with god and the word was god
the same was in the beginning with god all things were made by him and without
him was not any thing made that was made in him was life and the life was the
light of men and the light shineth in darkness and the darkness comprehended it not
there was a man sent from god whose name was john the same came for a witness
to bear witness of the light that all men through him might believe he was not
that light but was sent to bear witness of that light that was the true light
which lighteth every man that cometh into the world he was in the world and the
world was made by him and the world knew him not

Once upon a time there was a young girl who lived in the forest with her
grandmother the forest was deep and dark and full of wild animals the girl
loved to walk through the forest and pick flowers and berries she was kind
and gentle and all the animals of the forest loved her very much she would
often sing to the birds and they would sing back to her the rabbit and the
deer would come to her hand and she would feed them with bread and honey
the old grandmother told her stories of the ancient world and taught her the
names of all the trees and plants and stars in the night sky

The great fish moved silently through the night water propelled by short
sweeps of its crescent tail over the sharp stones and through the kelp
forests and beneath the thermoclines of warmer water the fish moved with
primal urgency through the ancient sea toward the shore where the waves
crashed against the rocks and the spray rose high into the air the gulls
circled above watching the water for signs of movement below

Four score and seven years ago our fathers brought forth on this continent
a new nation conceived in liberty and dedicated to the proposition that
all men are created equal now we are engaged in a great civil war testing
whether that nation or any nation so conceived and so dedicated can long endure
we are met on a great battlefield of that war we have come to dedicate a portion
of that field as a final resting place for those who here gave their lives that
that nation might live it is altogether fitting and proper that we should do this
but in a larger sense we can not dedicate we can not consecrate we can not hallow

We are all born mad some remain so the world is a stage and all the men
and women merely players they have their exits and their entrances and
one man in his time plays many parts his acts being seven ages at first
the infant mewling and puking in the nurse arms and then the whining schoolboy
with his satchel and shining morning face creeping like a snail unwillingly to
school and then the lover sighing like furnace with a woeful ballad made to
his mistress eyebrow then a soldier full of strange oaths and bearded like

It was a dark and stormy night the wind howled through the trees and the
rain beat against the windows inside the old house a fire burned brightly
casting warm shadows on the walls the family sat together in the small
room listening to the storm outside they were safe and warm and happy
together they told stories and laughed and drank hot chocolate while the
wind raged outside the children fell asleep one by one wrapped in blankets
by the fire and the parents sat watching them with love in their hearts

Knowledge is power and power is the ability to act in the world the
human mind is capable of extraordinary things when properly trained and
motivated people can achieve goals that seem impossible at first the key
to success is persistence and hard work combined with intelligence and creativity
every great achievement begins with a single step and the courage to take it
those who dare to try may fail but those who never try have already failed
the difference between success and failure is often just one more attempt

The sun also rises and there is no new thing under the sun all the rivers
run into the sea yet the sea is not full unto the place from whence the
rivers come thither they return again the wind goeth toward the south and
turneth about unto the north it whirleth about continually and the wind
returneth again according to his circuits all things are full of labour
man cannot utter it the eye is not satisfied with seeing nor the ear filled
with hearing what has been done is what will be done and there is nothing
new under the sun is there a thing of which it is said see this is new

Time present and time past are both perhaps present in time future and
time future contained in time past if all time is eternally present all
time is unredeemable what might have been is an abstraction remaining a
perpetual possibility only in a world of speculation what might have been
and what has been point to one end which is always present footfalls echo
in the memory down the passage which we did not take towards the door we
never opened into the rose garden my words echo thus in your mind

The old man sat alone in his boat far out at sea he had not caught a
fish in eighty four days and now he was truly and deeply and humbly
alone but he did not mind being alone and he was not afraid for he
was a fisherman and the sea was his home and he loved it well and the
boy was helpful and kind and the old man taught him everything he knew
about the sea and about fishing and about life itself they were the best
of friends despite the great difference in their ages the old man said
everything about him was old except his eyes and they were the same color
as the sea and were cheerful and undefeated

If you can keep your head when all about you are losing theirs and
blaming it on you if you can trust yourself when all men doubt you
but make allowance for their doubting too if you can wait and not
be tired by waiting or being lied about do not deal in lies
or being hated do not give way to hating and yet look good
nor talk too wise if you can dream and not make dreams your master
if you can think and not make thoughts your aim if you can meet
with triumph and disaster and treat those two impostors just the same
yours is the earth and everything that is in it

The road goes ever on and on down from the door where it began now
far ahead the road has gone and i must follow if i can pursuing it
with weary feet until it joins some larger way where many paths and
errands meet and whither then i cannot say a traveller must be ready
for the journey and must carry with him hope and courage and the will
to see what lies beyond the next hill and the next valley for the world
is full of wonders and the road goes ever on

Technology has transformed the world in ways that were unimaginable just
decades ago the internet has connected billions of people across the globe
machine learning and artificial intelligence are now solving problems that
once seemed beyond the reach of human ingenuity the future holds even
greater changes that will reshape how we live and work and communicate
with each other neural networks can learn patterns from vast amounts of
data and make predictions that rival human experts in many fields the
applications range from medical diagnosis to self driving cars to language
translation and far beyond what we can imagine today

In data science and machine learning the quality of your training data
determines the quality of your model the algorithm is only as good as
the information it learns from and the predictions are only useful if
the model has been properly validated on held out test data the performance
of the model depends on the diversity and size of the training corpus
a model trained on a small dataset will not generalize well to new examples
the process of building a good model involves careful feature engineering
data cleaning cross validation hyperparameter tuning and iterative testing
the best models are those that balance complexity with generalization

The best way to predict the future is to create it the world is changed
by people who do not wait for permission to act they see what needs to
be done and they do it the great leaders of history were not people who
followed the crowd they were people who saw further and acted faster
than anyone else around them they had vision and determination and the
courage to stand alone when necessary the future belongs to those who
believe in the beauty of their dreams and work every day to make them real

Love is patient love is kind it does not envy it does not boast it is not
proud it is not rude it is not self seeking it is not easily angered it keeps
no record of wrongs love does not delight in evil but rejoices with the truth
it always protects always trusts always hopes always perseveres love never fails
but where there are prophecies they will cease where there are tongues they will
be stilled where there is knowledge it will pass away for we know in part and
we prophesy in part but when completeness comes what is in part disappears

The quick brown fox jumps over the lazy dog and the dog did not seem to mind
at all because the fox was its friend they had grown up together in the same
yard and spent many happy afternoons chasing each other through the tall grass
beneath the old oak tree where the sun filtered through the leaves making
patterns of light and shadow on the ground below every day they would play
until the sun went down and then they would curl up together and sleep

In a hole in the ground there lived a hobbit not a nasty dirty wet hole filled
with the ends of worms and an oozy smell nor yet a dry bare sandy hole with
nothing in it to sit down on or to eat it was a hobbit hole and that means comfort
it had a perfectly round door like a porthole painted green with a shiny yellow
brass knob in the exact middle the door opened on to a tube shaped hall like a
tunnel a very comfortable tunnel without smoke with panelled walls and floors
tiled and carpeted provided with polished chairs and lots and lots of pegs for hats

It is not our abilities that show what we truly are it is our choices that
define us and shape the world around us every day we make hundreds of small
decisions that add up to the kind of person we become the habit of making
good choices leads to a good life and the habit of making poor choices leads
to regret and missed opportunities we must be mindful of each choice we make
for it is the accumulation of our daily decisions that determines our destiny
character is not born but built one choice at a time through years of practice

The morning sun rises over the mountains casting long shadows across the valley
below birds sing in the trees and the air is fresh and cool after the night rain
a farmer walks through his fields checking on the crops that he planted last spring
hoping for a good harvest in the autumn when the leaves turn red and gold the earth
is rich and dark and the seeds he planted are growing strong and tall reaching
toward the light of the sun the seasons turn and each one brings its own beauty
and its own challenges and the farmer knows that patience and hard work will be
rewarded when the harvest comes at last

Science and reason are the tools with which we understand the universe we live in
by careful observation and systematic testing we can discover the laws that govern
nature and use that knowledge to improve the lives of all people on earth the
scientific method has given us medicine technology and understanding beyond measure
the universe is vast and ancient and full of mysteries waiting to be explored
every discovery leads to new questions and new possibilities for understanding
the fundamental nature of reality from the smallest particles to the largest
structures in the cosmos the pursuit of knowledge is the noblest endeavor

The city never sleeps its streets alive with the hum of a million conversations
taxis honk and weave through traffic while pedestrians stream across crosswalks
in waves the neon lights of times square paint the night in electric colors
vendors sell hot dogs on every corner and the subway rumbles beneath the ground
carrying millions of people to their destinations the skyline stretches upward
a forest of glass and steel reaching toward the clouds each building a monument
to human ambition and engineering the city is a living breathing organism that
grows and changes with every passing day and night

The ocean stretched before her vast and endless a mirror of silver under the
moonlight she stood at the edge of the pier feeling the salt breeze on her face
and listening to the gentle rhythm of the waves the lighthouse in the distance
sent its beam sweeping across the water a silent guardian of the coast she
thought about all the ships that had sailed these waters and all the stories
they carried with them the sea holds secrets that no one will ever know and
she found comfort in that mystery in the vastness of something beyond understanding

Music filled the room a soft melody drifting from the old piano in the corner
his fingers moved across the keys with practiced ease each note hanging in the
air for a moment before fading into the next the audience sat in silence
captivated by the beauty of the performance outside the rain fell steadily
against the windows creating a gentle percussion that accompanied the music
perfectly it was one of those rare moments when everything comes together
and the world feels exactly as it should be pure and simple and beautiful

The laboratory was quiet except for the hum of the machines and the soft click
of the keyboard the scientist stared at the screen her eyes scanning the data
that scrolled before her years of research had led to this moment the algorithm
had finally converged and the results were better than anyone had expected the
model could predict with remarkable accuracy and the implications were enormous
she leaned back in her chair and smiled knowing that this breakthrough would
change the field forever the future of artificial intelligence had just taken
a giant leap forward

Education is the most powerful weapon which you can use to change the world
the purpose of education is not just to fill a pail but to light a fire
a good teacher can inspire hope ignite the imagination and instill a love
of learning that lasts a lifetime the classroom is where the future begins
every student deserves the chance to discover their potential and to develop
the skills they need to succeed in a rapidly changing world reading opens
doors to new worlds and new ideas and mathematics teaches us to think clearly
and solve problems with precision and creativity

The garden was peaceful in the early morning light dew drops glistened on the
petals of roses and the bees were already busy moving from flower to flower
the old gardener knelt in the soft earth his hands working carefully around
the roots of a young tomato plant he had been tending this garden for forty
years and he knew every inch of the soil every plant was like a friend to him
and he spoke to them softly as he worked the seasons came and went but the
garden remained his constant companion his source of joy and purpose

History is not just a record of the past it is a guide for the future those
who do not learn from history are condemned to repeat it the great civilizations
of the ancient world rose and fell each leaving behind lessons for those who
would come after the romans built roads and aqueducts that still inspire engineers
today the greeks gave us democracy and philosophy and the foundations of western
thought the egyptians constructed monuments that have endured for thousands of
years reminding us that human creativity and determination know no bounds

The train pulled into the station with a long slow hiss of steam passengers
gathered their belongings and stepped onto the platform into the cold morning
air the conductor called out the station name and checked his pocket watch
it was exactly seven thirty two right on schedule the old station had seen
millions of travellers pass through its doors each one carrying their own
story their own hopes and dreams and fears the departures board clicked and
spun announcing the next train to the coast and a new group of passengers
began to gather on the platform

The stars above were countless points of light scattered across the velvet
darkness of the sky she lay on the grass and gazed upward trying to comprehend
the immensity of the universe each star a sun perhaps with planets of its own
orbiting in the eternal dance of gravity the milky way stretched across the sky
a river of light that our ancestors once told stories about every culture in
the world has looked up at these same stars and wondered what they mean and
where we fit in the grand tapestry of existence it was humbling and beautiful
and she felt both very small and very connected to everything at once
"""

# ═══════════════════════════════════════════════
#  LSTM MODEL — pure numpy
# ═══════════════════════════════════════════════

class Tokenizer:
    def __init__(self, tokens):
        freq = Counter(tokens)
        self.word2idx = {"<PAD>": 0}
        self.idx2word = {0: "<PAD>"}
        for i, (word, _) in enumerate(freq.most_common(), start=1):
            self.word2idx[word] = i
            self.idx2word[i] = word
        self.vocab_size = len(self.word2idx)

    def add_word(self, word):
        if word not in self.word2idx:
            idx = self.vocab_size
            self.word2idx[word] = idx
            self.idx2word[idx] = word
            self.vocab_size += 1
            return True
        return False

    def encode(self, words):
        return [self.word2idx.get(w, 0) for w in words]


class LSTMModel:
    def __init__(self, vocab_size, embed_dim=48, hidden_dim=64):
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.hidden_dim = hidden_dim

        def xavier(fi, fo):
            lim = np.sqrt(6.0 / (fi + fo))
            return np.random.uniform(-lim, lim, (fi, fo))

        self.embedding = xavier(vocab_size, embed_dim)
        self.Wlstm = xavier(embed_dim + hidden_dim, 4 * hidden_dim)
        self.blstm = np.zeros(4 * hidden_dim)
        self.blstm[hidden_dim:2*hidden_dim] = 1.0
        self.Wy = xavier(hidden_dim, vocab_size)
        self.by = np.zeros(vocab_size)

    def expand_vocab(self, new_size):
        if new_size <= self.vocab_size:
            return
        old = self.vocab_size
        le = np.sqrt(6.0 / (new_size + self.embed_dim))
        ly = np.sqrt(6.0 / (self.hidden_dim + new_size))
        new_e = np.random.uniform(-le, le, (new_size, self.embed_dim))
        new_e[:old] = self.embedding
        self.embedding = new_e
        new_W = np.random.uniform(-ly, ly, (self.hidden_dim, new_size))
        new_W[:, :old] = self.Wy
        self.Wy = new_W
        self.by = np.concatenate([self.by, np.zeros(new_size - old)])
        self.vocab_size = new_size

    def _sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-np.clip(x, -15, 15)))

    def _softmax(self, x):
        e = np.exp(x - np.max(x))
        return e / (e.sum() + 1e-10)

    def forward_sequence(self, indices):
        T, H = len(indices), self.hidden_dim
        embeds, gates_cache = [], []
        h_s = [np.zeros(H)]
        c_s = [np.zeros(H)]
        for t in range(T):
            x = self.embedding[indices[t]]
            embeds.append(x)
            xh = np.concatenate([x, h_s[-1]])
            g = xh @ self.Wlstm + self.blstm
            i = self._sigmoid(g[:H])
            f = self._sigmoid(g[H:2*H])
            gc = np.tanh(np.clip(g[2*H:3*H], -15, 15))
            o = self._sigmoid(g[3*H:4*H])
            c = f * c_s[-1] + i * gc
            h = o * np.tanh(np.clip(c, -15, 15))
            h_s.append(h); c_s.append(c)
            gates_cache.append((i, f, gc, o, xh, c_s[-2]))
        return h_s, c_s, embeds, gates_cache

    def predict(self, indices, top_k=5):
        if not indices:
            return []
        h_s, _, _, _ = self.forward_sequence(indices)
        probs = self._softmax(h_s[-1] @ self.Wy + self.by)
        top = np.argsort(probs)[::-1][:top_k]
        return [(int(i), float(probs[i])) for i in top]

    def train_step(self, inp, tgt, lr=0.01):
        T, H = len(inp), self.hidden_dim
        h_s, c_s, embeds, gc = self.forward_sequence(inp)
        loss = 0.0
        dWy, dby = np.zeros_like(self.Wy), np.zeros_like(self.by)
        dWl, dbl = np.zeros_like(self.Wlstm), np.zeros_like(self.blstm)
        dh_n, dc_n = np.zeros(H), np.zeros(H)
        de = {}
        for t in reversed(range(T)):
            h = h_s[t+1]
            probs = self._softmax(h @ self.Wy + self.by)
            loss += -np.log(probs[tgt[t]] + 1e-10)
            dl = probs.copy(); dl[tgt[t]] -= 1.0
            dWy += np.outer(h, dl); dby += dl
            dh = dl @ self.Wy.T + dh_n
            i, f, g, o, xh, cp = gc[t]
            tc = np.tanh(np.clip(c_s[t+1], -15, 15))
            do = dh * tc
            dc = dh * o * (1 - tc**2) + dc_n
            di, df, dg = dc * g, dc * cp, dc * i
            dc_n = dc * f
            dgs = np.concatenate([di*i*(1-i), df*f*(1-f), dg*(1-g**2), do*o*(1-o)])
            dWl += np.outer(xh, dgs); dbl += dgs
            dxh = dgs @ self.Wlstm.T
            dh_n = dxh[self.embed_dim:]
            idx = inp[t]
            if idx not in de: de[idx] = np.zeros(self.embed_dim)
            de[idx] += dxh[:self.embed_dim]
        for gr in [dWy, dby, dWl, dbl]: np.clip(gr, -5, 5, out=gr)
        self.Wy -= lr*dWy; self.by -= lr*dby
        self.Wlstm -= lr*dWl; self.blstm -= lr*dbl
        for idx, gr in de.items():
            np.clip(gr, -5, 5, out=gr)
            self.embedding[idx] -= lr*gr
        return loss / T

    def fine_tune(self, inp, tgt, lr=0.005, passes=3):
        for _ in range(passes):
            self.train_step(inp, tgt, lr=lr)


def train_model(corpus_text, seq_len=8, epochs=8, lr=0.02, progress_cb=None):
    tokens = [w for w in re.sub(r'[^a-z\s]', ' ', corpus_text.lower()).split() if w]
    tok = Tokenizer(tokens)
    enc = tok.encode(tokens)
    model = LSTMModel(tok.vocab_size)
    seqs = [enc[i:i+seq_len+1] for i in range(0, len(enc)-seq_len, 2)]
    total = epochs * len(seqs)
    step = 0
    for ep in range(epochs):
        random.shuffle(seqs)
        el, n = 0.0, 0
        for s in seqs:
            el += model.train_step(s[:-1], s[1:], lr=lr)
            n += 1; step += 1
            if progress_cb and step % 50 == 0:
                progress_cb(step/total, ep+1, epochs, el/n)
        lr *= 0.85
    return model, tok, tokens


# ═══════════════════════════════════════════════
#  SESSION STATE & TRAINING
# ═══════════════════════════════════════════════

import json, os

SESSION_FILE = "user_session.json"

def save_session():
    """Persist user words to disk so they survive refresh."""
    data = {
        "words": st.session_state.words,
        "total": st.session_state.total,
        "hits": st.session_state.hits,
        "near_hits": st.session_state.near_hits,
        "learned": st.session_state.learned,
    }
    with open(SESSION_FILE, "w") as f:
        json.dump(data, f)

def load_session():
    """Load previous session if it exists."""
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return None

if "custom_corpus" not in st.session_state:
    st.session_state.custom_corpus = None
if "model_trained" not in st.session_state:
    st.session_state.model_trained = False

corpus_text = st.session_state.custom_corpus or DEFAULT_CORPUS

if not st.session_state.model_trained:
    st.markdown('<p class="app-header">Can I Guess Your Next Word? <span class="app-tag">LSTM</span></p>', unsafe_allow_html=True)
    st.markdown('<p class="app-sub">Training the neural network...</p>', unsafe_allow_html=True)
    bar = st.progress(0)
    status = st.empty()

    def on_progress(pct, ep, total_ep, loss):
        bar.progress(min(pct, 1.0))
        status.markdown(f'<div class="train-info">Epoch {ep}/{total_ep} · Loss: {loss:.3f} · {pct*100:.0f}%</div>', unsafe_allow_html=True)

    model, tokenizer, tokens = train_model(corpus_text, progress_cb=on_progress)
    st.session_state.model = model
    st.session_state.tokenizer = tokenizer
    st.session_state.tokens = tokens
    st.session_state.model_trained = True
    bar.empty(); status.empty()

    # Replay saved session to re-learn user patterns
    saved = load_session()
    if saved and saved.get("words"):
        for w in saved["words"]:
            if tokenizer.add_word(w):
                model.expand_vocab(tokenizer.vocab_size)
        # Fine-tune on saved words in chunks
        all_w = saved["words"]
        if len(all_w) >= 3:
            enc = tokenizer.encode(all_w)
            for i in range(0, len(enc) - 3, 2):
                chunk = enc[i:i+10]
                if len(chunk) >= 3:
                    model.fine_tune(chunk[:-1], chunk[1:], lr=0.008, passes=3)

    st.rerun()

model = st.session_state.model
tokenizer = st.session_state.tokenizer

DEFAULTS = {
    "words": [],
    "history": [],      # [{"word": str, "hit": bool/None, "near": bool, "preds": [...]}]
    "total": 0,
    "hits": 0,
    "near_hits": 0,     # word was in top 10 but not top 5
    "preds": [],
    "preds_extended": [],  # top 10 for near-miss checking
    "learned": 0,
    "user_bigrams": {},    # {"word1 word2": count} — what the model learned from you
}

# Initialize defaults FIRST (before loading session, which appends to history)
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v if not isinstance(v, (list, dict)) else (list(v) if isinstance(v, list) else dict(v))

# Load saved session on first run
if "session_loaded" not in st.session_state:
    st.session_state.session_loaded = True
    saved = load_session()
    if saved and saved.get("words"):
        st.session_state.words = saved["words"]
        st.session_state.total = saved.get("total", 0)
        st.session_state.hits = saved.get("hits", 0)
        st.session_state.near_hits = saved.get("near_hits", 0)
        st.session_state.learned = saved.get("learned", 0)
        # Rebuild history (simplified — no per-word preds on reload)
        for i, w in enumerate(saved["words"]):
            st.session_state.history.append({"word": w, "hit": None, "near": False, "preds": []})
        # Rebuild bigrams
        for i in range(len(saved["words"]) - 1):
            pair = f'{saved["words"][i]} → {saved["words"][i+1]}'
            st.session_state.user_bigrams = st.session_state.get("user_bigrams", {})
            st.session_state.user_bigrams[pair] = st.session_state.user_bigrams.get(pair, 0) + 1
        # Set predictions for next word
        if saved["words"]:
            enc = tokenizer.encode([w.lower() for w in saved["words"][-8:]])
            raw = model.predict(enc, top_k=10)
            all_preds = [(tokenizer.idx2word.get(i, ""), p) for i, p in raw if i != 0]
            st.session_state.preds = all_preds[:5]
            st.session_state.preds_extended = all_preds[:10]


def get_preds(context, top_k=10):
    if not context:
        return []
    enc = tokenizer.encode([w.lower() for w in context[-8:]])
    raw = model.predict(enc, top_k=top_k)
    return [(tokenizer.idx2word.get(i, ""), p) for i, p in raw if i != 0]


def submit_word(word):
    """Process a new word from the user."""
    w = re.sub(r'[^a-z]', '', word.lower())
    if not w:
        return

    if st.session_state.words:
        # Check top 5 (hit) and top 10 (near miss)
        top5 = [x[0] for x in st.session_state.preds]
        top10 = [x[0] for x in st.session_state.preds_extended]
        hit = w in top5
        near = (not hit) and (w in top10)

        st.session_state.total += 1
        if hit:
            st.session_state.hits += 1
        if near:
            st.session_state.near_hits += 1

        st.session_state.history.append({
            "word": w, "hit": hit, "near": near, "preds": st.session_state.preds[:5]
        })

        # Track bigram
        prev = st.session_state.words[-1]
        pair = f"{prev} → {w}"
        if "user_bigrams" not in st.session_state:
            st.session_state.user_bigrams = {}
        st.session_state.user_bigrams[pair] = st.session_state.user_bigrams.get(pair, 0) + 1
    else:
        st.session_state.history.append({"word": w, "hit": None, "near": False, "preds": []})

    st.session_state.words.append(w)

    # Expand vocab if new word
    if tokenizer.add_word(w):
        model.expand_vocab(tokenizer.vocab_size)

    # More aggressive fine-tuning
    recent = st.session_state.words[-12:]
    if len(recent) >= 3:
        enc = tokenizer.encode(recent)
        model.fine_tune(enc[:-1], enc[1:], lr=0.008, passes=5)
        st.session_state.learned += 1

    # Update predictions (get top 10, show top 5)
    all_preds = get_preds(st.session_state.words, top_k=10)
    st.session_state.preds = all_preds[:5]
    st.session_state.preds_extended = all_preds[:10]

    # Save to disk
    save_session()


def on_word_submit():
    typed = st.session_state.get("word_input", "").strip()
    if not typed:
        return
    for word in typed.split():
        submit_word(word)
    st.session_state.word_input = ""


# ═══════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════

with st.sidebar:
    st.markdown("### Settings")
    st.caption("Upload a .txt file to retrain the base model on different text.")
    uploaded = st.file_uploader("Upload .txt", type=["txt"], label_visibility="collapsed")
    if uploaded:
        txt = uploaded.read().decode("utf-8", errors="ignore")
        if txt.strip():
            st.session_state.custom_corpus = txt
            st.session_state.model_trained = False
            st.session_state.session_loaded = False
            for k in DEFAULTS: st.session_state[k] = DEFAULTS[k] if not isinstance(DEFAULTS[k], (list, dict)) else (list(DEFAULTS[k]) if isinstance(DEFAULTS[k], list) else dict(DEFAULTS[k]))
            if os.path.exists(SESSION_FILE): os.remove(SESSION_FILE)
            st.rerun()
    if st.session_state.custom_corpus:
        if st.button("Reset to default corpus"):
            st.session_state.custom_corpus = None
            st.session_state.model_trained = False
            st.session_state.session_loaded = False
            for k in DEFAULTS: st.session_state[k] = DEFAULTS[k] if not isinstance(DEFAULTS[k], (list, dict)) else (list(DEFAULTS[k]) if isinstance(DEFAULTS[k], list) else dict(DEFAULTS[k]))
            if os.path.exists(SESSION_FILE): os.remove(SESSION_FILE)
            st.rerun()
    st.markdown("---")
    st.caption(f"LSTM · {tokenizer.vocab_size:,} vocab · fine-tuned {st.session_state.learned}x on your input")


# ═══════════════════════════════════════════════
#  MAIN UI
# ═══════════════════════════════════════════════

st.markdown('<p class="app-header">Can I Guess Your Next Word? <span class="app-tag">LSTM</span></p>', unsafe_allow_html=True)
st.markdown('<p class="app-sub">Type one word at a time. I\'ll try to predict it. I learn from everything you type.</p>', unsafe_allow_html=True)

# Metrics
t = st.session_state.total
h = st.session_state.hits
nh = st.session_state.near_hits
acc = f"{h/t*100:.0f}%" if t > 0 else "—"
st.markdown(f"""
<div class="metric-row">
    <div class="metric-box"><div class="metric-val">{t}</div><div class="metric-label">Words</div></div>
    <div class="metric-box"><div class="metric-val">{h}</div><div class="metric-label">Predicted</div></div>
    <div class="metric-box"><div class="metric-val">{acc}</div><div class="metric-label">Accuracy</div></div>
    <div class="metric-box"><div class="metric-val">{nh}</div><div class="metric-label">Close</div></div>
</div>
""", unsafe_allow_html=True)

# Current predictions (only show after first word)
preds = st.session_state.preds
if preds and len(st.session_state.words) >= 1:
    mx = preds[0][1] if preds else 1
    rows = ""
    for i, (w, p) in enumerate(preds[:5]):
        bw = min(p / mx * 100, 100) if mx > 0 else 0
        rows += f"""<div class="pred-row">
            <div class="pred-rank">{i+1}</div>
            <div class="pred-word">{w}</div>
            <div class="pred-bar-bg"><div class="pred-bar-fill" style="width:{bw}%;"></div></div>
            <div class="pred-pct">{p*100:.1f}%</div>
        </div>"""
    st.markdown(f"""<div class="card">
        <div style="font-size:0.72rem;color:#9ca3af;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">I think your next word is...</div>
        {rows}
    </div>""", unsafe_allow_html=True)
elif not st.session_state.words:
    st.markdown("""<div class="card">
        <div style="color:#6b7280;font-size:0.9rem;">Type your first word to get started. I'll start predicting from the second word onward.</div>
    </div>""", unsafe_allow_html=True)

# Text input
input_label = "Start your sentence:" if not st.session_state.words else "Type your next word:"
st.text_input(input_label, value="", key="word_input",
              placeholder="type one word, press enter...",
              on_change=on_word_submit)

# Last result
if st.session_state.history:
    last = st.session_state.history[-1]
    if last["hit"] is None:
        pass
    elif last["hit"]:
        st.markdown(f"""<div class="card" style="background:#f0fdf4;border-color:#bbf7d0;">
            <span style="color:#059669;font-weight:600;">Got it.</span>
            <span style="color:#6b7280;"> "{last["word"]}" was in my top 5.</span>
        </div>""", unsafe_allow_html=True)
    elif last.get("near"):
        st.markdown(f"""<div class="card" style="background:#fffbeb;border-color:#fde68a;">
            <span style="color:#d97706;font-weight:600;">Close.</span>
            <span style="color:#6b7280;"> "{last["word"]}" was in my top 10 but not top 5.</span>
        </div>""", unsafe_allow_html=True)
    else:
        top3 = ", ".join([f'{w} ({p*100:.1f}%)' for w, p in last["preds"][:3]]) if last["preds"] else "—"
        st.markdown(f"""<div class="card" style="background:#fef2f2;border-color:#fecaca;">
            <span style="color:#dc2626;font-weight:600;">Missed.</span>
            <span style="color:#6b7280;"> You typed "{last["word"]}" — I predicted: {top3}</span>
        </div>""", unsafe_allow_html=True)

# Word history
if st.session_state.history:
    wh = ""
    for e in st.session_state.history:
        if e["hit"] is None:
            cls = "history-miss"
        elif e["hit"]:
            cls = "history-hit"
        elif e.get("near"):
            cls = "history-hit"  # near misses get green-ish too
        else:
            cls = "history-miss"
        wh += f'<span class="history-word {cls}">{e["word"]}</span> '
    st.markdown(f"""<div class="card">
        <div style="font-size:0.72rem;color:#9ca3af;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">Your text</div>
        <div style="line-height:2.0;">{wh}</div>
    </div>""", unsafe_allow_html=True)

# What I've learned
bigrams = st.session_state.get("user_bigrams", {})
if bigrams:
    sorted_bg = sorted(bigrams.items(), key=lambda x: x[1], reverse=True)[:8]
    patterns = ""
    for pair, count in sorted_bg:
        patterns += f'<span style="display:inline-block;background:#eff6ff;color:#2563eb;padding:3px 10px;border-radius:4px;margin:3px 4px;font-family:JetBrains Mono,monospace;font-size:0.8rem;">{pair} <span style="color:#9ca3af;">×{count}</span></span>'
    st.markdown(f"""<div class="card">
        <div style="font-size:0.72rem;color:#9ca3af;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">Patterns I've learned from you</div>
        <div style="line-height:2.2;">{patterns}</div>
        <div style="margin-top:8px;font-size:0.78rem;color:#9ca3af;">These are word pairs I've seen you type. The more I see a pattern, the better I predict it.</div>
    </div>""", unsafe_allow_html=True)

# Controls
st.markdown("---")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Clear & start over", use_container_width=True):
        for k in DEFAULTS: st.session_state[k] = DEFAULTS[k] if not isinstance(DEFAULTS[k], (list, dict)) else (list(DEFAULTS[k]) if isinstance(DEFAULTS[k], list) else dict(DEFAULTS[k]))
        st.session_state.preds = []
        st.session_state.preds_extended = []
        if os.path.exists(SESSION_FILE): os.remove(SESSION_FILE)
        st.rerun()
with c2:
    user_words = st.session_state.words
    has_enough = len(user_words) >= 5
    if st.button("Retrain with my words", use_container_width=True, disabled=not has_enough,
                 help="Need at least 5 words" if not has_enough else "Merges your words into the training corpus and retrains the model from scratch"):
        # Build augmented corpus: original corpus + user sentences repeated for emphasis
        user_text = " ".join(user_words)
        # Repeat user text a few times so it has real weight against the large corpus
        augmented = corpus_text + "\n" + (user_text + " ") * 5
        st.session_state.custom_corpus = augmented
        st.session_state.model_trained = False
        st.session_state.session_loaded = False
        # Keep the user's stats but reset history display (will rebuild on reload)
        old_total, old_hits, old_near, old_learned = (
            st.session_state.total, st.session_state.hits,
            st.session_state.near_hits, st.session_state.learned
        )
        old_words = list(st.session_state.words)
        old_bigrams = dict(st.session_state.get("user_bigrams", {}))
        for k in DEFAULTS: st.session_state[k] = DEFAULTS[k] if not isinstance(DEFAULTS[k], (list, dict)) else (list(DEFAULTS[k]) if isinstance(DEFAULTS[k], list) else dict(DEFAULTS[k]))
        # Restore stats so the user doesn't lose their score
        st.session_state.words = old_words
        st.session_state.total = old_total
        st.session_state.hits = old_hits
        st.session_state.near_hits = old_near
        st.session_state.learned = old_learned
        st.session_state.user_bigrams = old_bigrams
        # Rebuild history (simplified)
        for w in old_words:
            st.session_state.history.append({"word": w, "hit": None, "near": False, "preds": []})
        save_session()
        st.rerun()
with c3:
    if st.button("Full reset", use_container_width=True):
        st.session_state.model_trained = False
        st.session_state.session_loaded = False
        st.session_state.custom_corpus = None
        for k in DEFAULTS: st.session_state[k] = DEFAULTS[k] if not isinstance(DEFAULTS[k], (list, dict)) else (list(DEFAULTS[k]) if isinstance(DEFAULTS[k], list) else dict(DEFAULTS[k]))
        if os.path.exists(SESSION_FILE): os.remove(SESSION_FILE)
        st.rerun()
