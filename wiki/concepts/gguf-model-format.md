---
summary: A unified model file format developed by Georgi Gerganov for efficient storage
  and inference of quantized large language models.
tags:
- artificial-intelligence
- machine-learning
- model-formats
- quantization
- llama-cpp
- non-target
- category:other
title: GGUF Model Format / GGUF 模型格式 / GGUFモデルフォーマット
---

## English

**GGUF** (Georgi Gerganov Unified Format) is a model file format specifically designed for the efficient storage, distribution, and inference of quantized large language models. Developed by Georgi Gerganov, the creator of llama.cpp, GGUF represents a standardized approach to packaging machine learning models in ways that optimize both storage efficiency and runtime performance across diverse hardware configurations.

The format addresses several critical challenges in deploying large language models outside of cloud computing environments. Traditional model formats often assume the availability of substantial computational resources and memory, making them impractical for deployment on consumer hardware. GGUF overcomes these limitations by incorporating quantization specifications directly into the model file structure, enabling models to run on hardware with limited capabilities.

GGUF files contain the complete model architecture and parameters in a compressed format, including all necessary components for inference: model weights, vocabulary data, configuration parameters, and metadata. The format supports multiple quantization schemes, ranging from minimal compression (which preserves most model quality) to aggressive compression (which dramatically reduces resource requirements at the cost of some output quality degradation).

Key advantages of the GGUF format include:

- **Self-contained packaging**: All necessary components for model execution are included in a single file, simplifying distribution and deployment.
- **Hardware flexibility**: The format supports inference across various hardware configurations, from high-end GPUs to CPUs and even mobile processors.
- **Quantization integration**: Quantization parameters are embedded within the file, eliminating the need for separate quantization configuration.
- **Version stability**: The format includes version information that helps ensure compatibility between model files and inference engines.
- **Efficient memory mapping**: GGUF files support memory-mapped I/O operations, allowing the operating system to manage memory more efficiently.

The format has become a de facto standard for distributing quantized models in the open-source AI community, with widespread support across inference frameworks including llama.cpp, Ollama, and various other tools. Major model providers offer their models in GGUF format, recognizing the format's role in making powerful AI capabilities accessible to users without specialized hardware.

GGUF represents an important advancement in the democratization of AI technology. By enabling efficient model execution on commodity hardware, the format expands access to advanced AI capabilities beyond organizations with substantial computational resources, supporting educational applications, research projects, and individual experimentation with large language models.

## 中文

**GGUF**（Georgi Gerganov统一格式）是一种专门为量化大型语言模型的高效存储、分发和推理而设计的模型文件格式。该格式由llama.cpp的创建者Georgi Gerganov开发，代表了将机器学习模型打包以优化存储效率和运行时性能的标准化方法，适用于各种硬件配置。

该格式解决了在云计算环境之外部署大型语言模型的几个关键挑战。传统模型格式通常假定有大量计算资源和内存可用，这使得它们在消费级硬件上的部署变得不切实际。GGUF通过将量化规范直接整合到模型文件结构中来解决这些限制，使模型能够在能力有限的硬件上运行。

GGUF文件以压缩格式包含完整的模型架构和参数，包括推理所需的所有组件：模型权重、词汇数据、配置参数和元数据。该格式支持多种量化方案，从最小压缩（保留大部分模型质量）到激进压缩（以输出质量下降为代价大幅降低资源需求）。

GGUF格式的主要优势包括：

- **自包含打包**：模型执行所需的所有组件都包含在单个文件中，简化了分发和部署。
- **硬件灵活性**：该格式支持跨各种硬件配置的推理，从高端GPU到CPU甚至移动处理器。
- **量化集成**：量化参数嵌入在文件中，无需单独的量化配置。
- **版本稳定性**：该格式包含版本信息，有助于确保模型文件和推理引擎之间的兼容性。
- **高效的内存映射**：GGUF文件支持内存映射I/O操作，允许操作系统更高效地管理内存。

该格式已成为开源AI社区中分发量化模型的事实标准，获得llama.cpp、Ollama和各种其他工具的广泛支持。主要模型提供商以GGUF格式提供他们的模型，认识到该格式在使强大的AI能力对没有专门硬件的用户可访问方面的作用。

## 日本語

**GGUF**（Georgi Gerganov Unified Format）は、量子化された大規模言語モデルの効率的な保存、配布、推論のために特別に設計されたモデルファイル形式である。llama.cppの創設者であるGeorgi Gerganovによって開発されたGGUFは、多様なハードウェア構成間でストレージ効率とランタイムパフォーマンスを最適化する方法で機械学習モデルをパッケージ化する標準化されたアプローチを表している。

この形式は、クラウドコンピューティング環境外での大規模言語モデルの展開におけるいくつかの重要な課題に対処している。従来のモデル形式は、多くの場合、相当な計算リソースとメモリの利用可能性を前提としており、これによりコンシューマハードウェアへの展開が非現実的になる。GGUFは、量子化仕様をモデルファイル構造に直接組み込むことでこれらの制限を克服し、モデルの実行を能力が限られたハードウェアでも可能にする。

GGUFファイルには、モデル权重、词汇データ、設定パラメータ、メタデータを含む、推論に必要なすべてのコンポーネントが圧縮形式で含まれている。この形式は、最小圧縮（モデルの品質の大部分を保持）から積極的な圧縮（出力品質の低下を犠牲にしてリソース要件を大幅に削減）まで、複数の量子化スキームをサポートしている。