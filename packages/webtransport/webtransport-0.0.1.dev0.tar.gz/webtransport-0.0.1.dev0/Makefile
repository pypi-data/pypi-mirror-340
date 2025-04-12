PORT = 4433
HOST = localhost

.PHONY: all cert fingerprint clean show-flags

all: cert fingerprint show-flags server client

cert:
	@echo "Generating certificate and private key..."
	@openssl req -newkey rsa:2048 -nodes \
		-keyout certs/certificate.key \
		-x509 -out certs/certificate.pem \
		-subj '/CN=Test Certificate' \
		-addext "subjectAltName = DNS:$(HOST)"
	@chmod 600 certs/certificate.key
	@chmod 644 certs/certificate.pem

fingerprint: certs/certificate.key certs/certificate.pem
	@echo "Computing certificate fingerprint..."
	@openssl x509 -pubkey -noout -in certs/certificate.pem | \
		openssl rsa -pubin -outform der | \
		openssl dgst -sha256 -binary | base64 > certs/cert_fingerprint.txt

show-flags: fingerprint
	@echo "\nChrome flags to use:"
	@echo "--origin-to-force-quic-on=$(HOST):$(PORT)"
	@echo "--ignore-certificate-errors-spki-list=$$(cat certs/cert_fingerprint.txt)"

server: cert
	@echo "Starting server on port $(PORT)..."
	@python3 server/webtransport_server.py certs/certificate.pem certs/certificate.key

client: fingerprint
	@echo "Running Chrome with the generated certificate..."
	@google-chrome --origin-to-force-quic-on=$(HOST):$(PORT) \
		--ignore-certificate-errors-spki-list=$$(cat certs/cert_fingerprint.txt) \
		--user-data-dir=/tmp/chrome_test \
		--no-sandbox \
		--disable-web-security \
		--disable-extensions \
		--disable-gpu \
		client/index.html

clean:
	rm -f certs/certificate.key certs/certificate.pem certs/cert_fingerprint.txt
