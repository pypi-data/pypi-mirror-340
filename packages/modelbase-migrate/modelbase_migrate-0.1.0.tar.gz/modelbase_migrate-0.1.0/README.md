# modelbase-migrate

Migrate models between different modelbase versions (currently v1 -> v2).

## Installation

```bash
pip install modelbase-migrate
```

## Usage

```python
from modelbase_migrate import migrate

migrate(
    model_v1,
    initial_conditions={...},
    out_file=out / "model_name.py",
)
```
