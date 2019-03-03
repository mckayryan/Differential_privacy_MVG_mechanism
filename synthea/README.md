# Synthea<sup>TM</sup> Patient Generator [![Build Status](https://travis-ci.org/synthetichealth/synthea.svg?branch=master)](https://travis-ci.org/synthetichealth/synthea) [![codecov](https://codecov.io/gh/synthetichealth/synthea/branch/master/graph/badge.svg)](https://codecov.io/gh/synthetichealth/synthea)

Synthea<sup>TM</sup> is a Synthetic Patient Population Simulator. The goal is to output synthetic, realistic (but not real), patient data and associated health records in a variety of formats.

Read our [wiki](https://github.com/synthetichealth/synthea/wiki) for more information.

Currently, Synthea<sup>TM</sup> features:
- Birth to Death Lifecycle
- Configuration-based statistics and demographics (defaults with Massachusetts Census data)
- Modular Rule System
  - Drop in [Generic Modules](https://github.com/synthetichealth/synthea/wiki/Generic-Module-Framework)
  - Custom Java rules modules for additional capabilities
- Primary Care Encounters, Emergency Room Encounters, and Symptom-Driven Encounters
- Conditions, Allergies, Medications, Vaccinations, Observations/Vitals, Labs, Procedures, CarePlans
- Formats
  - FHIR (STU3 v3.0.1, DSTU2 v1.0.2 and R4)
  - C-CDA
  - CSV
- Rendering Rules and Disease Modules with Graphviz

## Quick Start

### Installation

**System Requirements:**
Synthea<sup>TM</sup> requires Java 1.8 or above.

To clone the Synthea<sup>TM</sup> repo, then build and run the test suite:
```
git clone https://github.com/synthetichealth/synthea.git
cd synthea
./gradlew build check test
```

### Generate Synthetic Patients
Generating the population one at a time...
```
./run_synthea
```

Command-line arguments may be provided to specify a state, city, population size, or seed for randomization.

Usage is 
```
run_synthea [-s seed] [-p populationSize] [state [city]]
```
For example:

 - `run_synthea Massachusetts`
 - `run_synthea Alaska Juneau`
 - `run_synthea -s 12345`
 - `run_synthea -p 1000`
 - `run_synthea -s 987 Washington Seattle`
 - `run_synthea -s 21 -p 100 Utah "Salt Lake City"`

Some settings can be changed in `./src/main/resources/synthea.properties`.

Synthea<sup>TM</sup> will output patient records in C-CDA and FHIR formats in `./output`.

### Synthea<sup>TM</sup> GraphViz
Generate graphical visualizations of Synthea<sup>TM</sup> rules and modules.
```
./gradlew graphviz
```

# License

Copyright 2017-2018 The MITRE Corporation

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
