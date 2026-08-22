#!/bin/sh
uv run taskiq worker src.core.broker:broker \
  --fs-discover \
  --tasks-pattern "src/**/tasks.py" \
  --no-configure-logging \
  --workers 2 \
  --shutdown-timeout 30 \
  --wait-tasks-timeout 30
