#!/bin/bash

main() {
	local dir="$1"
	local callback="$2"
	while true; do
		# run our tool first, so a container-restart would trigger it
		echo "Running web_video"
		date
		./web_video/run.py "$dir" "$callback"
		echo "Finished web_video $(date)"

		# first big inotifywait will detect, that an upload was started
		# but we then need to wait until everything is finished
		inotifywait -e close_write --recursive "$dir"
		while true; do
			# here we wait for the upload to finish
			if inotifywait --recursive --timeout 3600 "$dir"; then
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
