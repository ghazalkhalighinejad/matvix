<h1 align="center">MatViX: Multimodal Information Extraction from Visually Rich Articles</h1>

<p align="center">
  <a href="https://ghazalkhalighinejad.github.io/">Ghazal Khalighinejad</a> ·
  <a>Sharon Scott</a> ·
  <a href="https://ollieliu.com/">Ollie Liu</a> ·
  <a>Aman Tyagi</a> ·
  <a>Kelly Anderson</a> ·
  <a href="https://www.rickard.stureborg.com/">Rickard Stureborg</a> ·
  <a href="https://users.cs.duke.edu/~bdhingra/">Bhuwan Dhingra</a>
</p>

**MatViX** is a benchmark dataset and framework designed for multimodal information extraction from visually rich materials science articles. It focuses on extracting structured data from both text, tables, and figures in scientific documents.

# Modeling

Follow these instructions to extract structured data from the `PNC` and `PBD` documents.

## Environment Variable Setup
Before running the commands, make sure to export the necessary environment variables:

```bash
export PYTHONPATH="your_path_to_this_repo"
export OPENAI_API_KEY="your_openai_api_key"
export GOOGLE_API_KEY="your_gemini_api_key"
export ANTHROPIC_API_KEY="your_anthropic_api_key"
```

## For PNC
To model the PNC data, use the following command:
```bash
python3 pnc/main.py --resume --articles_path <path_to_articles> --model <model_name> --prompt_type <prompt_type> [--samples_path <path_to_samples>] [--deplot]
```

## For PBD
To model the PBD data, use the following command:
```bash
python3 pbd/main.py --resume --articles_path <path_to_articles> --model <model_name> --prompt_type <prompt_type> [--samples_path <path_to_samples>] [--deplot]
```

## Parameters
- **`--resume`**: Add this flag if you want to resume a previous run.
- **`--articles_path`**: Provide the path to the articles (e.g., `../datasets/pnc/articles/dataset/test`).
- **`--model`**: Choose from the following models:
  - `claude3`
  - `claude35`
  - `gpt4o`
  - `gpt4-turbo`
  - `gemini`
- **`--prompt_type`**: Options include:
  - `only-text`
  - `only-image_single-image`
  - If you choose `only-image`, you must also provide `--samples_path` with the path from the `only-text` run.
- **`--deplot`** (Optional): Add this flag if you want to use DePlot for processing figures.
