# **context window** 
---

## 1️⃣ **What is a Context Window?**

The **context window** is the *maximum number of tokens* a GPT model can process **at once** — including:

* **System prompt**
* **Your prompt** (user messages)
* **Conversation history** you send again in the request
* **Model’s own output**

If the conversation exceeds this token limit, older tokens are **dropped** or **truncated**.

---

## 2️⃣ **Why it exists**

GPT is a **transformer-based model**, and transformers process sequences of tokens in parallel.
The computational and memory cost of self-attention grows roughly **quadratically** with sequence length, so there’s a practical limit to how many tokens can be handled at once.

---

## 3️⃣ **How it works in practice**

Let’s say a model has a **context window of 8,000 tokens**.

Example:

* System prompt: 500 tokens
* Previous chat history: 6,000 tokens
* Your new question: 300 tokens
* Model’s answer: 1,200 tokens

**Total** = 500 + 6,000 + 300 + 1,200 = **8,000 tokens** ✅ (Fits within the limit)

If instead the total was **over 8,000 tokens**, the **oldest tokens** in history would be removed to make room for new ones.

---

## 4️⃣ **Context Window Sizes (examples)**

* **GPT-3.5 Turbo** → 4k or 16k tokens
* **GPT-4** → 8k or 32k tokens
* **GPT-4o** → \~128k tokens
* **Claude 3.5 Sonnet** → \~200k tokens
* **GPT-5** (rumored) → possibly 256k+ tokens

---

## 5️⃣ **What happens when you exceed it**

When the total number of tokens in the conversation > context window:

* The **oldest messages** get removed (if in chat mode)
* In API calls, if you pass too many tokens in the input, the request is rejected or truncated

**Important:** The model does not “remember” things removed from the context window — it’s gone unless you manually reinsert it in the prompt.

---

## 6️⃣ **Why it’s important**

* **Memory illusion** → GPT seems to “remember” past conversation only because the history is re-sent each time, within the window.
* **Long documents** → If you paste a 200k-token book into a 128k-token model, part of it will be cut off.
* **Pricing** → Bigger context windows cost more per request because more tokens = more compute.

---

## 7️⃣ **Analogy**

Imagine GPT’s memory as a **sliding window** on a scroll:

* It can only see a certain number of words (tokens) at a time.
* As new words come in, old ones fall off the back.
* The width of that window = **context window size**.
