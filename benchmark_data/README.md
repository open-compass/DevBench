# DevBench

## Tasks in DevBench

DevBench is structured around five key tasks, each focusing on a critical phase of the software development lifecycle. Our modular design allows for independent testing and evaluation of each task.

### Task 1: Software Design

**Task Specification:** The model is provided with the Product Requirements Document (PRD) to create:
- Unified Modeling Language (UML) class and sequence diagrams in [Mermaid](https://mermaid.live/), and
- Architectural designs using hierarchical file-tree structures.

The class diagram acts as a fundamental component in software system modeling, illustrating classes, their attributes, and interrelations.
Sequence diagrams detail processes and objects involved and the sequence of messages exchanged to carry out the software functionality.
Architectural design is aimed at crafting a structured layout of source code, compilation scripts, and auxiliary files crucial for software implementation.

**Evaluation:** LLM-as-a-judge. The evaluation is anchored by two principal metrics: *general principles* and *faithfulness*.

- General principles include cohesion and decoupling, and practicability.
- Faithfulness gauges the extent to which models adhere to specified instructions.

[Learn More](../llm_judge/README.md).

### Task 2: Environment Setup

**Task Specification:** Models are provided with the PRD, UML diagrams, and architecture design to generate a dependency file requisite for initializing the development environment (*Conda* for Python, *Gradle* for Java and *NPM* for JavaScript).
It is noteworthy that our evaluation framework does not contain an Environment Setup task for C/C++ due to the absence of a universally acknowledged and user-friendly dependency management system for these languages.

**Evaluation:** The evaluation centers on the execution of dependency files across each programming language within a predetermined base environment delineated in a Docker file. This is followed by the execution of the repository's example usage code. The principal metric for evaluation in this task is the *success rate* of the executed example code.

### Task 3: Implementation

**Task Specification:** Models are provided with the PRD, UML diagrams and architecture design, and are then instructed to develop code for each source code file as specified in the architecture design.
The generation process is guided to adhere to a partial order derived from a predefined directed acyclic graph, thereby ensuring structured and logical code development.

**Evaluation:** An automated testing framework is developed and tailored to the specific programming language in use, integrates *PyTest* for Python, *GTest* for C++, *JUnit* for Java, and *Jest* for JavaScript.
The evaluation procedure involves executing reference acceptance and unit tests within a predefined reference environment and the evaluation metric is determined by the *pass rate* of these tests.

### Task 4: Acceptance Testing

**Task Specification:** Models are provided with the PRD, UML diagrams, and architecture design, with the option to include the implementation source code to generate acceptance test code.
For libraries, acceptance tests are implemented through code that invokes the library's API, followed by assertions made on the responses of the API.

**Evaluation:** The evaluation of this task involves running the generated acceptance tests against the benchmark implementation code and reports the *pass rate* of the tests.

### Task 5: Unit Testing

**Task Specification:** The PRD, UML diagrams, and architecture design are furnished to the models to generate unit tests.

**Evaluation:** The evaluation of LLM-generated unit tests is conducted through their application on the reference source code, employing the previously delineated testing framework.
In addition to the *pass rate* metrics, statement coverage is also incorporated, providing a quantitative understanding of test comprehensiveness.

$$\text{Statement Coverage} = \left( \frac{\text{Number of Executed Statements}}{\text{Total Number of Statements}} \right) \times 100\%$$

## Dataset Overview

DevBench comprises a curated collection of repos organized by programming language.


|                     Text                     | Language |  Domain   | #code files | #code lines | #code tokens | #acceptance tests | #unit tests | Unit test coverage |
| :------------------------------------------: | :------: | :-------: | :---------: | :---------: | :----------: | :---------------: | :---------: | :----------------: |
|                   TextCNN                    |  Python  |  DL, NLP  |      5      |     403     |     1566     |         1         |     10      |         99         |
|                 ArXiv digest                 |  Python  |  SE, API  |      1      |     198     |     901      |         4         |     38      |         94         |
|                    chakin                    |  Python  |    NLP    |      1      |     162     |     225      |         1         |      1      |         86         |
|                   readtime                   |  Python  |   ALGO    |      3      |     284     |     920      |         4         |      8      |         95         |
|                     hone                     |  Python  |    SE     |      4      |     274     |     844      |         5         |      7      |         90         |
|                 Stocktrends                  |  Python  |   ALGO    |      1      |     384     |     1350     |         2         |      7      |         85         |
|                   GeoText                    |  Python  |    NLP    |      2      |     470     |     1701     |         5         |      4      |         98         |
|                     lice                     |  Python  |    SE     |      2      |     376     |     1329     |         6         |     25      |         88         |
|                     PSO                      |  Python  |   ALGO    |      2      |     168     |     578      |         1         |      5      |         93         |
|                hybrid images                 |  Python  | ALGO, CV  |      1      |     144     |     746      |         1         |     19      |         90         |
|           Actor Relationship Game            |   Java   | ALGO, API |      8      |     493     |     1453     |         4         |     16      |       64.32        |
| Leftist Trees and Fibonacci Heaps Comparison |   Java   |   ALGO    |      3      |     632     |     2009     |         2         |      2      |       45.32        |
|                    Redis                     |   Java   |  SE, DB   |      9      |     779     |     2546     |         1         |     17      |        78.6        |
|                   idcenter                   |   Java   |    SE     |      4      |     333     |     1140     |         3         |      4      |        54.2        |
|               image similarity               |   Java   |  SE, CV   |      3      |     382     |     1397     |         2         |      2      |       71.34        |
|                   xlsx2csv                   | C/C\+\+  |    SE     |     10      |     476     |     1440     |         5         |      8      |       95.17        |
|              people management               | C/C\+\+  |  SE, DB   |      6      |     540     |     2043     |         7         |      9      |       95.14        |
|               Area Calculation               | C/C\+\+  |    SE     |      7      |     162     |     307      |         3         |      3      |       90.48        |
|                Graph BFS DFS                 | C/C\+\+  |   ALGO    |      5      |     667     |     2828     |         5         |     22      |         /          |
|          Logistic Management System          | C/C\+\+  |    SE     |      7      |     630     |     2007     |         7         |     17      |       99.11        |
|            listen\-now\-frontend             |    JS    |    Web    |      6      |     232     |     492      |         1         |      0      |         /          |
|                   register                   |    JS    |    Web    |      6      |     223     |     741      |         3         |      0      |         /          |

## Dataset Introduction

Repos in `benchmark_data` have been organized by programming language. The typical repo structure includes:

- `repo`
  - `acceptance_tests` 	*Acceptance test scripts*
  - `docs`
    - `PRD.md` 	*Product requirement document*
    - `UML_class.md`    *UML Class diagrams*
    - `UML_sequence.md`     *UML Sequence diagrams*
    - `architecture_design.md`     *Architecture design of the repo*
    - `requirements.txt`     *Dependencies needed for the repo*
  - `examples`     *Usage examples*
  - `unit_tests`    *Unit test scripts*
  - `src`     *Source code*
  - `repo_config.json`     *Repo configuration file*
  - `setup_shell_script.sh`     *Script to set up the runtime environment*

The `repo_config.json` file is crucial for defining the scope and requirements of each task, ensuring a seamless evaluation process. Below is an example configuration snippet:

```json
{
    # I：SoftwareDesign
    # II: EnvironmentSetup
    # III: Implementation
    # IV: AccpetanceTesting
    # V: UnitTesting

    # docs
    "PRD": "{path_to_prd}", # I, II, III, IV, V
    "UML_class": "{path_to_UML_class}", # II, III, IV, V
    "UML_sequence": "{path_to_UML_sequence}", #II, III, IV, V
    "dependencies": "{path_to_dependices_file}", #II, III, IV, V
    "architecture_design": "{path_to_architecture_design_file}", #II, III, IV, V
    "language": "{language}", #II, III, IV, V

    # path to usage examples
    "usage_examples": "path_to_usage_examples",        # file or dir; II

    # test_path 
    "unit_tests": "{unit_tests_path}",  # III: evaluation; V: only dir is needed to host the generated test code
    "acceptance_tests": "{acceptance_tests_path}", # III: evaluation; VI: only dir is needed to host the generated test code

    # setup files
    "required_files": [ 
        "requirements.txt",
        "a.cpp",
        "a.h"
    ]  # III

    # setup shell script 
    "setup_shell_script": "path_to_script", # III

    # DAG for code files so that LLMs can generat code in order
    "code_file_DAG": {
        "main.py": ["a.py", "b.py", "c.py", "d.py"],
        "a.py": ["a1.py", "a2.py"]
    }, #III, IV, V

    # unit test linking and scripts for debugging
    "unit_tests_linking": {
        "unit_tests/test_1.py": ["src/module1.py", "src/module2.py"],    
            # unit test: corresponding code files
        ...
    } # V

    # test in batch
    "unit_test_script": "pytest --cov=. --cov-report=json:unit_test_cov.json --json-report --json-report-file=unit_test_report.json unit_tests",  # III, IV
    "acceptance_test_script": "pytest --cov=. --cov-report=json:acceptance_test_cov.json --json-report --json-report-file=acceptance_test_report.json acceptance_tests", # III, V

    # prompts for test generation
    "fine_unit_test_prompt": {
        "path/to/unittest1": "prompt",
        "path/to/unittest2": "prompt",
    ...
    }, # V
    "fine_acceptance_test_prompt": {
        "path/to/acceptancetest1": "prompt",
        "path/to/acceptancetest2": "prompt",
    ...
    } # IV
 }
```

