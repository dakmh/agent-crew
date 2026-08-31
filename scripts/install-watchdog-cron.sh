#!/bin/sh
# Register the unattended-run watchdog with cron (Linux) or launchd (macOS).
#
# A healthy run makes every firing a no-op; a stalled one gets restarted from
# its run log. See scripts/watchdog.py for what that means and does not mean.
#
#   ./install-watchdog-cron.sh --project /path/to/repo [--interval 20]
#                              [--stale-after 1200] [--python python3]
#                              [--notify-cmd "..."] [--dry-run] [--uninstall]
#
# On macOS the machine must be awake or the job simply does not run; `caffeinate
# -s` in another terminal, or Energy Saver set to never sleep on power, is what
# makes an overnight run possible. This script reports rather than changes that,
# the same as its Windows counterpart.

set -eu

PROJECT=""
INTERVAL=20
STALE=1200
PYTHON="python3"
NOTIFY=""
DRY=0
UNINSTALL=0
TAG="agent-crew-watchdog"

while [ $# -gt 0 ]; do
    case "$1" in
        --project)     PROJECT="$2"; shift 2 ;;
        --interval)    INTERVAL="$2"; shift 2 ;;
        --stale-after) STALE="$2"; shift 2 ;;
        --python)      PYTHON="$2"; shift 2 ;;
        --notify-cmd)  NOTIFY="$2"; shift 2 ;;
        --dry-run)     DRY=1; shift ;;
        --uninstall)   UNINSTALL=1; shift ;;
        *) echo "unknown argument: $1" >&2; exit 2 ;;
    esac
done

[ -n "$PROJECT" ] || { echo "--project is required" >&2; exit 2; }

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
WATCHDOG="$SCRIPT_DIR/watchdog.py"
[ -f "$WATCHDOG" ] || { echo "watchdog.py not found at $WATCHDOG" >&2; exit 2; }
PROJECT=$(CDPATH= cd -- "$PROJECT" && pwd)

CMD="$PYTHON \"$WATCHDOG\" --project \"$PROJECT\" --stale-after $STALE"
[ -n "$NOTIFY" ] && CMD="$CMD --notify-cmd \"$NOTIFY\""

if [ "$UNINSTALL" -eq 1 ]; then
    crontab -l 2>/dev/null | grep -v "$TAG" | crontab -
    echo "removed cron entries tagged $TAG"
    exit 0
fi

LINE="*/$INTERVAL * * * * cd \"$PROJECT\" && $CMD >> \"$PROJECT/.agent-crew/watchdog.out\" 2>&1 # $TAG"

echo "project  : $PROJECT"
echo "cadence  : every $INTERVAL minutes"
echo "crontab  : $LINE"
echo

case "$(uname -s)" in
    Darwin) echo "macOS: cron works, but the machine must stay awake. Check Energy Saver, or"
            echo "       run 'caffeinate -s' for the duration of the run." ; echo ;;
esac

if [ "$DRY" -eq 1 ]; then
    echo "dry run - nothing installed."
    exit 0
fi

mkdir -p "$PROJECT/.agent-crew"
( crontab -l 2>/dev/null | grep -v "$TAG"; echo "$LINE" ) | crontab -
echo "installed."
echo
echo "Fire it once before relying on it - an untested trigger is indistinguishable"
echo "from a working one until the night it matters:"
echo "    $CMD --dry-run"
echo
echo "Remove it when the run is done:"
echo "    $0 --project \"$PROJECT\" --uninstall"
