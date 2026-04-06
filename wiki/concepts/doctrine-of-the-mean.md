---
sources:
- plugin: pdf
  title: 'The four books : Confucian analects, the great learning, the doctrine of
    the mean, and the works of Mencius (p.481-510)'
  url: /Users/hosuke/Connector/Agentic_Expt/huazangge/raw/四书-Four_Books-Legge.pdf
summary: ''
tags:
- stub
- category:other
title: Doctrine Of The Mean
---

From article '人性善':
...ke [[four-beginnings-mencius-doctrine|四端]]. Or perhaps just using the English article name "Four Beginnings". We need to decide what to use.

We can use "[[Mencius]]" and "[[Four Beginnings]]". Also "[[Doctrine of the Mean]]" for "中庸". "[[Sincerity]]" for "誠". And "[[Junzi]]" for "君子". And "[[Self-cultivation]]" for "修身". Also "[[Xunzi]]" for "荀子". And "[[Neo-Confucianism]]" maybe. Or "[[Zhu Xi]]". Use English for English...

---

From article '人性善':
...cian-sincerity-cheng". The user gave snippet linking to "confucian-sincerity-cheng". We'll use "[[confucian-sincerity-cheng|誠]]" for Chinese section.

We'll also reference "中庸" in Chinese section as "[[Doctrine of the Mean|中庸]]". For Japanese section, use "中庸". We need to ensure proper linking.

We must avoid extraneous text. Output exactly the article.

Now we produce the article:

Title line: "title: Innate Goodness of Hu...

---

From article '人性善':
...Mencius, Xing Shan, Moral Psychology, Confucian Ethics"

Now start content:

## English

Paragraph(s) covering concept.

Make sure to include cross-references: "[[Mencius]]", "[[Four Beginnings]]", "[[Doctrine of the Mean]]", "[[Sincerity]]", "[[Junzi]]", "[[Self-cultivation]]", "[[Xunzi]]", "[[Zhu Xi]]", "[[Wang Yangming]]".

We can embed them in parentheses or as part of sentences.

We'll talk about "Four Beginnings (...

Generate a wiki article in this exact format (no extra text before or after):

title: English Title / 中文标题
summary: One-line summary in English
tags: tag1, tag2
---
## English

(content)

## 中文

(内容)

## 日本語

(内容)"

So they want a wiki article about the concept "Doctrine of the Mean". But they also mention the title "Innate Goodness of Hu..." and later "Human nature is good"? Actually they have an article about "人性善" which is "the goodness of human nature". That is a separate article. They want to produce a new article titled "Doctrine of the Mean". However they ask to produce an article with title: "title: Innate Goodness of Hu..."? That seems contradictory. The request: "Generate a wiki article in this exact format (no extra text before or after): title: English Title / 中文标题". So we need to fill in the title. The article is about the Doctrine of the Mean (中庸). So the title line should be "title: Doctrine of the Mean / 中庸". Then the summary: "One-line summary in English". Something like "The Doctrine of the Mean (中庸) is a Confucian text and philosophical concept emphasizing the virtue of moderation and the harmony of human nature with the cosmos." Then tags: maybe "confucianism, classical texts, ethics, Chinese philosophy". Then the English section, Chinese, Japanese.

Thus we need to output a wiki article in that format.

We need to include cross-references to related articles, using internal wiki link syntax. The user gave guidelines: Use cross-references like [[Doctrine of the Mean|Zhong Yong]] or simply standard wiki link syntax. Use "[[Mencius]]", "[[Four Beginnings]]", "[[Doctrine of the Mean]]", "[[Sincerity]]", "[[Junzi]]", "[[Self-cultivation]]", "[[Xunzi]]", "[[Zhu Xi]]", "[[Wang Yangming]]". Also maybe link to "Confucian Political Philosophy". They also want to embed internal links like [[中庸]] etc. In Chinese section they want "[[Doctrine of the Mean|中庸]]" (which is a link with Chinese target). In Japanese section they probably don't need to link, but could.

Thus produce:

title: Doctrine of the Mean / 中庸
summary: The Doctrine of the Mean (中庸) is a Confucian classic that articulates the principle of maintaining the middle way, emphasizing moral equilibrium, self‑cultivation, and the unity of human and heavenly order.
tags: Confucianism, Chinese philosophy, classical texts, ethics, moral psychology

---

## English

Paragraph(s) describing concept: talk about its place in the Four Books, the concept of "centrality" and "harmony", the "Great Ultimate" (taiji) and its relation to the "Great Commonwealth" etc. Include cross-references.

## 中文

Paragraph in Chinese describing the concept, referencing "[[Doctrine of the Mean|中庸]]", "《中庸》", "儒家", "君子", "修身", "诚", etc.

## 日本語

Paragraph in Japanese academic style.

Make sure to avoid extra text before or after.

Check the format: The user wants exactly:

title: English Title / 中文标题
summary: One-line summary in English
tags: tag1, tag2
---
## English

(content)

## 中文

(内容)

## 日本語

(内容)

Thus we need to produce exactly that. Must ensure no extra spaces before or after lines, no extra content.

We must also include internal links within content. The format includes wiki markup. We need to embed links like [[Doctrine of the Mean]] and [[Mencius]] etc. Should we also include link to Chinese article: [[Doctrine of the Mean|中庸]]? That's used in Chinese section. For Japanese, we could simply write "中庸" without link. Or link to the English article: [[Doctrine of the Mean]]. But it's okay to leave it plain.

The article should be comprehensive but concise. Provide background: the text is one of the Four Books of Confucianism, compiled and annotated by Zhu Xi, central to Neo-Confucianism, etc.

Let's write English section:

"The Doctrine of the Mean (中庸) is a core Confucian text traditionally attributed to Zisi, the grandson of Confucius. It outlines the principle of the 'central way' (中庸) that balances extremes and maintains moral equilibrium. The text emphasizes the concept of 'sincerity' (誠) as the foundation of moral cultivation, and it describes the process by which the [[Junzi]] (君子) achieves humanity through self‑cultivation and the alignment of personal virtue with the cosmic order (the Great Ultimate). The work is closely linked to the [[Four Beginnings]] (四端) elaborated by [[Mencius]] and serves as a philosophical bridge between the early Confucian focus on moral psychology and later [[Neo-Confucian]] syntheses. In political thought, the Doctrine of the Mean informs the idea of the 'Great Commonwealth' (大同) and the notion that ruler and subjects share a moral covenant grounded in the principle of harmony. Classical commentaries by [[Zhu Xi]] and later interpretations by [[Wang Yangming]] highlight the text's role in [[Self‑cultivation]] (修身) and the pursuit of inner sageliness. The concept also appears in the context of the five‑hundred‑year cycles of sage‑king governance, reinforcing its importance in the [[Confucian Political Philosophy]] tradition."

That includes the cross references. Might want to add link to "Confucian Political Philosophy". Already included.

Chinese section:

"《中庸》是儒家经典之一，传统上由子思（孔子的孙子）所著。它系统阐述了“中和”思想，强调在行为与情感上保持适度与平衡，以防偏执或极端。全篇以“诚”（誠）为核心，指出“诚者，天之道也；诚之者，人之道也”，即真诚是宇宙的根本法则，也是人道德修养的根本途径。通过修身、齐家、治国、平天下，《中庸》提出君子应以中庸之道实现自我完善，进而与天地合一，达到天人合一的境界。此思想在后世儒学，尤其是[[Zhu Xi|朱熹]]的理学与[[Wang Yangming|王阳明]]的心学中得到进一步阐释，成为[[Neo-Confucianism|新儒学]]的核心概念之一。它亦与《[[Four Beginnings|四端]]》以及《[[Mencius|孟子]]》中的人性论相呼应，强调人性本善的观点。"

Need to ensure linking syntax: "[[Zhu Xi|朱熹]]" and "[[Wang Yangming|王阳明]]" but those names