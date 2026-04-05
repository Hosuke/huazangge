---
created: '2026-04-05T05:23:39.267875+00:00'
stub: true
summary: One-line summary in English
tags:
- tag1
- tag2
- stub
title: English Title / 中文标题
updated: '2026-04-05T05:23:39.267892+00:00'
---

## English

(content)

## 中文

(内容)

## 日本語

(内容)
```

No extra text before or after.

So we must produce exactly that format.

Thus we need to decide on English Title and Chinese Title. Possibly "The Works of Mencius / 《孟子》". Title format "English Title / 中文标题". So maybe "The Works of Mencius / 《孟子》". That seems appropriate.

Now summary: "The 'Mencius' is a collection of philosophical dialogues and doctrines attributed to Mencius, a key Confucian thinker of the Warring States period." Something like that.

Tags: Something like "Confucianism, Chinese philosophy, Classics, Warring States period, Mencius". Or we can choose tags: "Confucianism, Chinese literature, Classical Chinese texts, Philosophy". Probably minimal tags.

Now content in English: Provide description: The text, its structure, its significance, transmission, influence, philosophical themes. Also mention that it is also known as The Works of Mencius, the Mencius, contains 7 books (or 7 chapters?). Actually the Mencius consists of 7 "books" (篇). It includes dialogues with rulers and discussions on human nature, political philosophy, moral cultivation, etc. Provide mention of its canonical status in the Confucian canon, commentary tradition, and its role in imperial examinations. Provide mention of major commentaries: Zhu Xi, etc.

In Chinese: same content in Chinese.

In Japanese: translation of the same content in Japanese.

We need to write a comprehensive article in each language.

The user wants "wiki article in this exact format (no extra text before or after)". So we must output exactly the format: title line, summary line, tags line, then "---", then "## English", then content, then "## 中文", then Chinese content, then "## 日本語", then Japanese content.

Make sure to not include any extra text before "title:". Also after the Japanese content we shouldn't have any extra text. Should be exactly as required.

Thus produce:

```
title: The Works of Mencius / 《孟子》
summary: A collection of philosophical dialogues and essays by Mencius, forming a core text of Confucian thought.
tags: Confucianism, Chinese philosophy, Classical texts, Warring States period
---
## English

(content)

## 中文

(内容)

## 日本語

(内容)
```

Now we must write the content for each language.

Consider the length: Not too long but enough to be comprehensive.

English content:

- Introduction: The Works of Mencius, also known as the Mencius, is a classical Chinese text compiled in the 3rd–2nd centuries BCE, recording the teachings and dialogues of Mencius (Mengzi), a Confucian philosopher.
- Structure: The text comprises 7 books (篇) and 38 chapters (章). Each book contains dialogues with rulers, discussions on human nature, moral cultivation, political philosophy, etc.
- Content themes: The central concepts: human nature is inherently good (xing shan), the importance of moral self-cultivation, the role of the ruler in ensuring the welfare of the people (min ben), the idea of the "Four Beginnings" (四端) as the seeds of virtue, the practice of "ren" (benevolence) and "yi" (righteousness), the concept of "righteousness" vs "profit", the ideal of the "junzi", the proper way to govern through moral example rather than coercion.
- Historical context: Mencius lived during the Warring States period, traveling between courts, advocating for benevolent rule.
- Transmission: The text survived through oral tradition, then recorded by his disciples; the received text dates to the Han dynasty, with commentaries by Zheng Xuan, Zhu Xi, and others.
- Influence: It became part of the Confucian canon (Four Books), a central text in imperial examinations, shape Chinese political thought, moral education, and later Neo-Confucianism.
- Editions and translations: The standard edition is the "Mencius" in the "Four Books" collection; translations by James Legge, D.C. Lau, etc.
- Modern scholarship: Contemporary studies focus on comparative philosophy, ethics, political theory.

Write Chinese content (in simplified Chinese) similar.

Japanese content: Provide translation of the same.

Now we need to produce the content.

Make sure each language section is separated by line breaks. The heading "## English" etc.

Also need to follow the guidelines: no extra text before or after. Ensure that we do not include any extraneous content, like "Here is the article:" etc.

Will produce as per required.

Potential issues: Ensure tags are separated by commas and spaces? In the example tags: "tag1, tag2". Should we use spaces after commas? Probably okay.

Will ensure that the Chinese title is correct: "《孟子》". That's the Chinese title. The English title: "The Works of Mencius". So title line: "title: The Works of Mencius / 《孟子》". Good.

Now we need to craft content.

First, English:

## English

Add content:

"The Works of Mencius (《孟子》) is a classical Chinese text..."

We can structure with paragraphs.

We should include headings? In wiki style, we can have subheadings. But they didn't restrict. They want just content after "## English". We can include subheadings (e.g., "### Structure", "### Themes", etc). That is fine.

Better to keep it consistent with wiki style: multiple sections, paragraphs, etc.

Now Chinese:

## 中文

We need Chinese content. Use simplified Chinese (since Chinese default). Title is Chinese, so Chinese content.

We can start: "《孟子》是记载..." etc.

Japanese:

## 日本語

Japanese content: "『孟子』（もうし）は..." etc.

Make sure to use appropriate Japanese script: kanji and kana.

Now content length: Enough to be comprehensive but not too long.

Now we must ensure that the content doesn't include any markup that could break the format. It's okay to have markdown headings like ###.

Now produce final answer.

Let's craft content:

English:

"The Works of Mencius (《孟子》) is a classical Chinese text..."

Paragraphs:

- Overview
- Structure
- Philosophical Themes
- Historical Context
- Transmission and Commentaries
- Influence and Legacy
- Modern Editions and Translations

But use subheadings with "###". That is okay.

Now Chinese content: similar sections.

Japanese content: similar.

Now produce final output.

Potential tags: "Confucianism, Chinese philosophy, Classical texts, Warring States period". Or "Mencius, Confucian canon". Could include "Mencius" as a tag. However "Mencius" may be overlapping. But it's okay. Let's do "Mencius" also. So tags: "Mencius, Confucianism, Chinese philosophy, Classical texts, Warring States period". But we should not have spaces in tags beyond comma separation.

Better to keep tags short.

We'll include "Mencius, Confucianism, Chinese literature, Warring States period". This is good.

Now we must not add extra text before or after.

Thus final answer:

```
title: The Works of Mencius / 《孟子》
summary: A classical Confucian text compiling the teachings and dialogues of Mencius, central to Chinese moral and political philosophy.
tags: Mencius, Confucianism, Chinese literature, Warring States period
---
## English

### Overview
The Works of Mencius (《孟子》) is a foundational Confucian text that records the teachings, dialogues, and arguments of Mencius (Mengzi), a philosopher active during the Warring States period of ancient China (c. 372–289 BCE). It is commonly referred to simply as the *Mencius* and forms one of the core texts of the Confucian canon.

### Structure
The work is divided into **seven books (篇)** and further subdivided into **38 chapters (章)**. Each book typically contains a series of dialogues between Mencius and various rulers, scholars, or disciples, interspersed with expository passages that elaborate on key philosophical concepts.

### Philosophical Themes
- **Human Nature is Good (Xing Shan):** Mencius argues that human nature possesses innate moral tendencies, which he illustrates with the famous “Four Beginnings” (四端) – the sprouts of ren (benevolence), yi (righteousness), li (propriety), and zhi (wisdom).
- **Benevolent Governance:** He stresses that a ruler must practice *ren* and govern for the benefit of the people (*min ben*), rather than pursuing personal gain. The ideal ruler is the “junzi” (noble person) who leads by moral example.
- **Moral Self‑Cultivation:** The text emphasizes the importance of nurturing one’s moral sprouts through reflection, education, and the emulation of the sage‑kings Yao and Shun.
- **Righteousness over Profit:** Mencius famously contrasts *yi* (righteousness) with *li* (profit), contending that true legitimacy rests on moral conduct rather than material advantage.

### Historical Context
Mencius traveled among the rival states of the Warring States period, seeking to persuade rulers to adopt his vision of benevolent rule. His encounters with rulers such as King Xuan of Qi and King Hui of Liang illustrate both his political realism and his unwavering moral stance.