# Copyright 2016 Grant Gould
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

TESTS = distributions/test/distribution_test.py \
        distributions/test/operations_test.py \
        model/test/markdown_test.py

PYS = $(shell git ls-tree -r HEAD . --name-only | grep py$$ )

SAMPLES = $(shell git ls-files -c samples/)

RESULTSDIR = .results

DEPSFILE = python_requirements.txt


.DELETE_ON_ERROR:
all: check_deps test pep8 nocrash pylint
clean:
	rm -rf $(RESULTSDIR)


# Test to verify that all declared dependencies are present, as version
# shear can cause seriously hard-to-debug failures.
.PHONY: check_deps
check_deps : $(DEPSFILE)
	! (pip3 freeze | diff - $< | grep '^>')


# Linter rule for pep8
.PHONY: pep8
pep8 : $(PYS)
	pep8 $(PYS)

# Linter rule for pylint
.PHONY: pylint
pylint : $(PYS)
	pylint $(PYS)


# Run all declared unit tests.
TEST_RESULTS = $(patsubst %,$(RESULTSDIR)/%.out,$(TESTS))

.PHONY: test
test: $(TEST_RESULTS)
$(RESULTSDIR)/%.out : % $(PYS) $(DEPSFILE)
	mkdir -p $(dir $@)
	PYTHONPATH=. $< > $@


# For each sample file, verify that cost.py does not crash when running it.
SAMPLE_NOCRASHES_HTML = $(patsubst %,$(RESULTSDIR)/%.html,$(SAMPLES))
SAMPLE_NOCRASHES_TXT = $(patsubst %,$(RESULTSDIR)/%.txt,$(SAMPLES))

.PHONY: nocrash
nocrash: $(SAMPLE_NOCRASHES_HTML) $(SAMPLE_NOCRASHES_TXT)
$(RESULTSDIR)/%.html : % $(PYS) $(DEPSFILE)
	mkdir -p $(dir $@)
	./cost.py --report=enhanced_html $< > $@
$(RESULTSDIR)/%.txt : % $(PYS) $(DEPSFILE)
	mkdir -p $(dir $@)
	./cost.py --report=structure_dump $< > $@

# display_cdf sometimes requires user intervention, so don't run it.
