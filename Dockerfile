FROM alpine:3.15 AS download
RUN apk add --no-cache curl && \
	curl -Ljo bento4.zip  https://www.bok.net/Bento4/binaries/Bento4-SDK-1-6-0-639.x86_64-unknown-linux.zip && \
	unzip bento4.zip && \
	mv Bento4-SDK-1-6-0-639.x86_64-unknown-linux/ bento4

FROM python:3.9

WORKDIR /
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*
COPY --from=download bento4/ bento4
ENV PATH=${PATH}:/bento4/bin:/bento4/utils
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./web_video ./web_video
