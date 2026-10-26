1. Problem: The script cannot be executed because it does not have execute permission.

Solution:

chmod +x scripts/health_check.sh
./scripts/health_check.sh

Alternatively, run it with Bash:

bash scripts/health_check.sh

2. Problem: The logs directory does not exist.

Solution:

mkdir -p logs

The monitoring script also creates this directory automatically.

3. Problem: The script may contain a syntax error.

Solution:

bash -n scripts/health_check.sh

No output usually means the syntax check passed. This does not confirm that every command will run successfully.