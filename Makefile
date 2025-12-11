build_mosquitto:
	docker build -f Dockerfile.mosquitto -t mosquitto-2.0.7 .

run_mosquitto:
	docker run -it --rm -p 1883:1883 mosquitto-2.0.7
	
fuzz:
	docker compose up --build

fuzz-hrotti:
	python fuzz.py config_hrotti.txt

run-hrotti:
	docker run --rm -p 1883:1883 newpronik/hrotti:latest

triage-hrotti:
	python triage.py crashes/mosquitto_vuln-1765486714.77743 config_hrotti.txt