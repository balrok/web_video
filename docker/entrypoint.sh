#!/bin/bash

main() {
	local dir="$1"
	local callback="$2"
	while true; do
		# run our tool first, so a container-restart would trigger it
		echo "$(date) Running web_video"
		./web_video/run.py "$dir" "$callback"
		echo "$(date) Finished web_video"

		# first inotifywait will detect, that an upload was started
		# but we then need to wait until everything is finished
		inotifywait -e close_write --recursive "$dir"
		while true; do
			# here we wait for the upload to finish - if we go in a timeout, it means nothing happened for some time
			if inotifywait --recursive --timeout 360 "$dir"; then
				echo "Got another file event - still waiting for the upload finished"
			else
				echo "Didn't get a new file event for some time - upload probably finished"
			fi
		done
	done
}

if [[ -n "$1" ]]; then
	DIR="$1"
fi
if [[ -n "$2" ]]; then
	CALLBACK="$2"
fi

if [[ -z "$DIR" ]]; then
	echo "You need to specify a directory with env-var DIR"
	exit 1
fi
if [[ ! -d "$DIR" ]]; then
	echo "Your specified directory '${DIR}' does not exist"
	exit 1
fi

main "$DIR" "$CALLBACK"
