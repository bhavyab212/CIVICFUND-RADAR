FUZZTIME ?= 10s

.PHONY: validate validate-product-cli validate-examples validate-recall dogfood-agent fuzz-smoke secret-scan

validate:
	cd cli/civicfund-radar && go test ./...
	python3 scripts/validate_example_outputs.py

validate-product-cli:
	cd cli/civicfund-radar && go build -o /tmp/civicfund-radar ./cmd/civicfund-radar
	python3 scripts/validate_product_surface.py --check-cli /tmp/civicfund-radar

validate-examples:
	python3 scripts/validate_example_outputs.py
	python3 scripts/validate_openprose_mirror_portability.py

validate-recall: validate-product-cli
	python3 scripts/validate_recall_audit.py --binary /tmp/civicfund-radar

dogfood-agent: validate-product-cli validate-examples validate-recall
	python3 scripts/validate_agent_dogfood.py --binary /tmp/civicfund-radar

fuzz-smoke:
	cd cli/civicfund-radar && go test -run=^$$ -fuzz=FuzzParseAssignment -fuzztime=$(FUZZTIME) ./internal/civicfundradar
	cd cli/civicfund-radar && go test -run=^$$ -fuzz=FuzzParseFeedItems -fuzztime=$(FUZZTIME) ./internal/civicfundradar
	cd cli/civicfund-radar && go test -run=^$$ -fuzz=FuzzParseGrantsXMLZip -fuzztime=$(FUZZTIME) ./internal/civicfundradar
	cd cli/civicfund-radar && go test -run=^$$ -fuzz=FuzzOpportunityFromFederalRegister -fuzztime=$(FUZZTIME) ./internal/civicfundradar
	cd cli/civicfund-radar && go test -run=^$$ -fuzz=FuzzSelectJSONFields -fuzztime=$(FUZZTIME) ./internal/cli
	cd cli/civicfund-radar && go test -run=^$$ -fuzz=FuzzEnsureReadOnlySQL -fuzztime=$(FUZZTIME) ./internal/cli

secret-scan:
	gitleaks detect --source . --redact --no-banner
	gitleaks detect --source . --no-git --redact --no-banner
