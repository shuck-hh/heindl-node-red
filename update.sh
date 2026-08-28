#!/usr/bin/env bash

set -u

REPOSITORY_ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
REMOTE=${REMOTE:-origin}
BRANCH=${BRANCH:-main}
RESTART_COMMAND=${"sudo reboot":-}

show_error() {
	 yad --error --title="Update failed" --text="$1" 2>/dev/null || printf 'Update failed: %s\n' "$1" >&2
}

if ! command -v git >/dev/null 2>&1; then
	show_error "git is required."
	exit 1
fi

if ! command -v yad >/dev/null 2>&1; then
	printf 'yad is required.\n' >&2
	exit 1
fi

cd -- "$REPOSITORY_ROOT" || {
	show_error "Could not access $REPOSITORY_ROOT."
	exit 1
}

if ! git fetch --quiet "$REMOTE" "$BRANCH"; then
	show_error "Could not check GitHub for updates."
	exit 1
fi

if git diff --quiet HEAD "$REMOTE/$BRANCH"; then
	yad --info --title="No update available" --text="The local files are already up to date." 2>/dev/null
	exit 0
fi

if ! yad --question --title="Update available" \
	--text="New files are available from GitHub. Update this folder now?" \
	--button="gtk-cancel:1" --button="gtk-ok:0"; then
	exit 0
fi

if ! git reset --hard --quiet "$REMOTE/$BRANCH"; then
	show_error "Could not replace the local files with the GitHub version."
	exit 1
fi

if yad --question --title="Update complete" \
	--text="The files were updated. Restart the application now?" \
	--button="gtk-cancel:1" --button="gtk-ok:0"; then
	if [[ -n "$RESTART_COMMAND" ]]; then
		if ! bash -c "$RESTART_COMMAND"; then
			show_error "The update succeeded, but the restart command failed."
			exit 1
		fi
	else
		yad --info --title="Restart required" \
			--text="The update succeeded. Restart the application manually." 2>/dev/null
	fi
fi
