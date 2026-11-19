
 echo "cloning git repo locally.."
 git clone https://github.com/marioreale/eosc-basic-compliance.git
 cd eosc-basic-compliance
 echo "verifying installation....."
 uv sync --locked
 uv run pytest -q                
 uv run ruff check src tests
 uv run basic-check points
 echo
 echo "running the test suite now...."
 uv run basic-check run

