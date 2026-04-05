---
summary: Google's open-source family of lightweight, state-of-the-art AI models designed
  for responsible AI development and efficient deployment.
tags:
- artificial-intelligence
- google-ai
- open-source-models
- text-generation
- gemma-family
- non-target
title: Gemma AI Model / Gemma AI 模型 / Gemma AIモデル
---

## English

**Gemma** is a family of open-source AI models developed by Google DeepMind, representing Google's commitment to democratizing access to powerful machine learning capabilities while maintaining responsible AI development practices. The Gemma model family includes several variants optimized for different computational constraints and use cases, ranging from compact models suitable for edge devices to larger models capable of sophisticated reasoning and generation tasks.

The Gemma models are designed with a focus on responsible AI development, incorporating safety measures and ethical considerations throughout the development pipeline. Unlike some proprietary models, Gemma's open-source nature allows researchers, developers, and organizations to inspect, fine-tune, and deploy the models according to their specific requirements while maintaining transparency about the model's capabilities and limitations.

The Gemma family includes multiple model sizes, each designated by parameter counts that indicate the model's complexity and capacity:

- **Gemma 2B**: A compact model with approximately 2 billion parameters, optimized for deployment on resource-constrained devices and real-time applications where latency is critical.
- **Gemma 4B**: A mid-range variant with around 4 billion parameters, offering improved performance while maintaining reasonable computational requirements.
- **Gemma 7B**: A larger model with approximately 7 billion parameters, capable of more sophisticated reasoning and generation tasks.
- **Gemma 26B and Gemma 31B**: High-capacity variants designed for applications requiring advanced reasoning capabilities, though with correspondingly higher computational demands.

Gemma models support text generation tasks, including conversational interactions, content creation, summarization, and various natural language processing applications. The models can process text inputs and generate contextually appropriate responses, making them suitable for integration into chatbots, writing assistants, and educational tools.

To make Gemma models accessible to users without high-end computing hardware, the models are available in quantized formats compatible with GGUF (Georgi Gerganov Unified Format). These quantized versions significantly reduce the model's memory footprint and computational requirements, enabling execution on consumer-grade hardware including laptops without dedicated GPUs. This accessibility approach aligns with the broader goal of making AI technology available to a wider audience.

The Gemma 4 release introduced enhanced capabilities including support for audio and image inputs alongside text, along with an expanded context window of up to 256,000 tokens. This represents a significant advancement over earlier versions, enabling more complex multi-modal interactions and the ability to process much longer documents and conversations.

For deployment with Ollama, Gemma models are available through the `ollama pull gemma4` command, with specific variants accessible through tags such as `gemma4:e2b`, `gemma4:e4b`, and others. This integration allows users to easily download and run Gemma models locally without managing complex model files or configuration settings.

## 中文

**Gemma** 是由Google DeepMind开发的开源AI模型系列，代表了Google在 democratizing 强大机器学习能力访问方面的承诺，同时保持负责任的AI开发实践。Gemma模型系列包括针对不同计算约束和使用场景优化的多个变体，从适合边缘设备的紧凑模型到能够执行复杂推理和生成任务的大型模型。

Gemma模型的设计注重负责任的AI开发，在整个开发流程中整合了安全措施和伦理考量。与一些专有模型不同，Gemma的开源性质允许研究人员、开发者和组织根据其特定需求检查、微调和部署模型，同时保持对模型能力和限制的透明度。

Gemma系列包括多个模型规模，每个规模由参数数量指定，表明模型的复杂性和容量：

- **Gemma 2B**：一个约20亿参数的紧凑模型，针对资源受限设备和延迟关键型实时应用进行了优化。
- **Gemma 4B**：一个约40亿参数的中端变体，在保持合理计算要求的同时提供改进的性能。
- **Gemma 7B**：一个约70亿参数的大型模型，能够执行更复杂的推理和生成任务。
- **Gemma 26B 和 Gemma 31B**：高容量变体，专为需要高级推理能力的应用而设计，尽管具有相应的更高计算需求。

Gemma模型支持文本生成任务，包括对话交互、内容创建、摘要和各种自然语言处理应用。模型可以处理文本输入并生成上下文适当的响应，使其适合集成到聊天机器人、写作辅助工具和教育工具中。

为了使Gemma模型对没有高端计算硬件的用户可访问，模型以与GGUF（Georgi Gerganov统一格式）兼容的量化格式提供。这些量化版本显著减少了模型的内存占用和计算要求，使得在消费级硬件（包括没有专用GPU的笔记本电脑）上执行成为可能。

Gemma 4版本引入了增强功能，包括支持音频和图像输入以及文本，以及扩展到256,000个标记的上下文窗口。这代表了相对于早期版本的重大进步，实现了更复杂的多模态交互以及处理更长文档和对话的能力。

## 日本語

**Gemma**は、Google DeepMindが開発したオープンソースAIモデルファミリーであり、強力な機械学習機能へのアクセスの民主化に対するGoogleのコミットメントを表すと共に、責任あるAI開発実践を維持している。Gemmaモデルファミリーには、異なる計算制約とユースケースに最適化された複数のバリアントが含まれており、エッジデバイスに適したコンパクトなモデルから、洗練された推論や生成タスクを実行できる大型モデルまで対応している。

Gemmaモデルは、責任あるAI開発に重点を置いて設計されており、開発パイプライン全体を通じて安全対策と倫理的考慮事項を組み込んでいる。一部のプロプライエタリモデルとは異なり、Gemmaのオープンソース性質により、研究者、開発者、組織はモデルの機能と限界について透明性を維持しながら、特定の要件に応じてモデルを検査、微調整、展開することができる。

Gemmaファミリーには、モデルの複雑さと容量を示すパラメータ数で指定された複数のモデルサイズが含まれている：

- **Gemma 2B**：約20億パラメータを持つコンパクトモデルで、リソース制約のあるデバイスやレイテンシが重要なリアルタイムアプリケーションに最適化されている。
- **Gemma 4B**：約40億パラメータを持つミッドレンジバリアントで、合理的な計算要件を維持しながらパフォーマンスを向上させている。
- **Gemma 7B**：約70億パラメータを持つ大型モデルで、より洗練された推論や生成タスクを実行できる。
- **Gemma 26BおよびGemma 31B**：高度な推論能力を必要とするアプリケーション向けに設計された高容量バリアントで、対応する計算要件も高い。

Gemmaモデルは、テキスト生成タスク，支持对话交互、内容创建、摘要和各种自然语言处理应用。モデルはテキスト入力を処理し、コンテキスト的に適切な応答を生成できるため、チャットボット、ライティングアシスタント、教育ツールへの統合に適している。

的高端计算硬件的用户，模型以与GGUF（Georgi Gerganov统一格式）兼容的量化格式提供。这些量化版本显著减少了模型的内存占用和计算要求，使得在消费级硬件上执行成为可能。