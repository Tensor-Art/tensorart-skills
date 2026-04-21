# TensorArt Skills

AI Agent Skills for [TensorArt](https://tensor.art)/[吐司](https://tusi.cn/) — Easily integrate TensorArt's AI image and video generation capabilities into your AI Agent.

## Overview

**tensorart-skills** bridges AI Agents and the [TensorArt OpenAPI](https://tensor.art), enabling agents to browse available generation tools, submit tasks, and retrieve image or video results — all through simple Python scripts with no external dependencies.

## Available Skills

| Skill | Description |
|-------|-------------|
| **tensorart-generate** | Browse tools, submit generation tasks, upload reference files, poll for results, and download outputs |

## Installation

```bash
npx skills add https://github.com/Tensor-Art/tensorart-skills --skill tensorart-generate
```

Obtain your Access Key from your personal profile on [TensorArt](https://tensor.art)/[吐司](https://tusi.cn/).

Then save your Access Key:

```bash
echo "your-access-key" > ~/.tensor_access_key
```

## How It Works

The agent follows a straightforward pipeline:

1. **List tools** — fetch all available generation tools with their inputs, outputs, and estimated compute cost
2. **Upload files** *(if needed)* — upload local reference images or videos before creating a task
3. **Create task** — submit the selected tool and inputs to start generation
4. **Poll status** — query the task every few seconds until it reaches a terminal state
5. **Download results** — save the generated image or video locally

## Project Structure

```
tensorart-skills/
├── README.md
├── LICENSE
└── skills/
    └── tensorart-generate/
        ├── SKILL.md
        └── scripts/
            ├── _api.py               # Auth and HTTP helpers
            ├── list_tools.py         # Fetch available tools
            ├── create_task.py        # Submit a generation task
            ├── query_task.py         # Poll task status
            ├── upload_file.py        # Upload a file to Cloudflare R2
            └── download_result.py    # Download output files locally
```

## Script Reference

<details>

**Prerequisites:** Python 3.6+, Access Key at `~/.tensor_access_key`

```bash
# List all available tools
python3 skills/tensorart-generate/scripts/list_tools.py

# Create a task
python3 skills/tensorart-generate/scripts/create_task.py "toolName" '[{"type":"STRING","value":"a cat"}]'

# Query task (single)
python3 skills/tensorart-generate/scripts/query_task.py <taskId>

# Query task (poll until done, 3s interval)
python3 skills/tensorart-generate/scripts/query_task.py <taskId> --poll

# Upload a file
python3 skills/tensorart-generate/scripts/upload_file.py /path/to/image.png

# Download a result
python3 skills/tensorart-generate/scripts/download_result.py <url> [output-path]
```

</details>

## Contributing

1. Create a new folder under `skills/`
2. Add a `SKILL.md` and a `scripts/` directory
3. Update the skills table above

## License

[MIT](LICENSE) © 2026 [Tensor-Art](https://github.com/Tensor-Art)
