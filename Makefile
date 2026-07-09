.PHONY: help
help:
	@echo "Socratic Garden commands:"
	@echo "  make init"
	@echo "  make clarify TOPIC='...'"
	@echo "  make ux TOPIC='...'"
	@echo "  make design TOPIC='...'"
	@echo "  make plan-docs TOPIC='...'"
	@echo "  make draft TOPIC='...' [FILE='path/to/brief.md']"
	@echo "  make review FILE='path/to/doc.md'"

.PHONY: init
init:
	python -m socratic_garden init

.PHONY: clarify
clarify:
	python -m socratic_garden clarify --topic "$(TOPIC)"

.PHONY: ux
ux:
	python -m socratic_garden ux --topic "$(TOPIC)"

.PHONY: design
design:
	python -m socratic_garden design --topic "$(TOPIC)"

.PHONY: plan-docs
plan-docs:
	python -m socratic_garden plan-docs --topic "$(TOPIC)"

.PHONY: draft
draft:
	python -m socratic_garden draft --topic "$(TOPIC)" $(if $(FILE),--file "$(FILE)",)

.PHONY: review
review:
	python -m socratic_garden review --file "$(FILE)"
