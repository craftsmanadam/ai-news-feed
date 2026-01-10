# All our targets are phony (no files to check), so performance should increase if implicit rule search is skipped.
.PHONY: bootstrap clean analyze_code analyze_image build unit_tests watch_unit_tests acceptance_tests test verify start stop

bootstrap:
	./bin/bootstrap.sh
clean:
	./bin/clean.sh
analyze_code: bootstrap
	./bin/analyze_code.sh
format:
	./bin/format.sh
build: bootstrap
	./bin/build.sh
analyze_image: build
	./bin/analyze_image.sh
unit_tests: bootstrap
	./bin/unit_tests.sh
watch_unit_tests: bootstrap
	./bin/watch_unit_tests.sh
test: unit_tests
verify: clean analyze_code unit_tests
start: build
	./bin/start.sh
stop:
	./bin/stop.sh
