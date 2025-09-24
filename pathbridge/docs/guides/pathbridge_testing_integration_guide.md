# PathBridge Testing Integration Guide

## Overview

PathBridge automated testing system generates comprehensive test suites using AI, supporting TDD methodology with >90% coverage and >80% mutation score.

**Supported Frameworks:**
- **Python**: pytest, unittest
- **JavaScript**: Jest, Mocha
- **Java**: JUnit, TestNG
- **Go**: testing package
- **C#**: xUnit, NUnit

## Quick Start

### 1. Basic Test Generation

```python
from pathbridge.testing.test_generator import TestGenerator, TestRequest

async def generate_tests():
    generator = TestGenerator()
    
    request = TestRequest(
        source_file="src/user_service.py",
        test_framework="pytest",
        coverage_target=90,
        mutation_score_target=80
    )
    
    result = await generator.generate_test_suite(request)
    
    print(f"Generated {len(result.test_cases)} test cases")
    print(f"Coverage: {result.coverage_achieved}%")
```

### 2. Integration with PATH Agents

```python
from pathbridge.agents.test_strategist import TestStrategistAgent

class TDDAgent(CoreAgent):
    def __init__(self):
        super().__init__("tdd_agent", phase=2, ["generate_tests"])
        self.test_generator = TestGenerator()
    
    async def execute_capability(self, request: CapabilityRequest) -> CapabilityResponse:
        if request.capability_name == "generate_tests":
            return await self._generate_comprehensive_tests(request.parameters)
    
    async def _generate_comprehensive_tests(self, params: Dict[str, Any]) -> Dict[str, Any]:
        # Generate unit tests
        unit_tests = await self.test_generator.generate_unit_tests(
            source_code=params["source_code"],
            business_rules=params["business_rules"]
        )
        
        # Generate integration tests
        integration_tests = await self.test_generator.generate_integration_tests(
            components=params["components"],
            api_specs=params["api_specs"]
        )
        
        return {
            "unit_tests": unit_tests,
            "integration_tests": integration_tests,
            "coverage_report": await self._calculate_coverage(unit_tests, integration_tests)
        }
```

## Test Generation Strategies

### Unit Test Generation

```python
from pathbridge.testing.generators import UnitTestGenerator

async def generate_unit_tests():
    generator = UnitTestGenerator()
    
    # Analyze source code
    source_analysis = await generator.analyze_source_code("src/calculator.py")
    
    # Generate tests for each function
    test_cases = []
    for function in source_analysis.functions:
        tests = await generator.generate_function_tests(
            function=function,
            test_types=["normal", "edge_cases", "error_conditions"],
            assertions_per_test=3
        )
        test_cases.extend(tests)
    
    return test_cases

# Example generated test
"""
def test_divide_normal_case():
    calculator = Calculator()
    result = calculator.divide(10, 2)
    assert result == 5.0
    assert isinstance(result, float)
    assert result > 0

def test_divide_by_zero():
    calculator = Calculator()
    with pytest.raises(ZeroDivisionError):
        calculator.divide(10, 0)
"""
```

### Integration Test Generation

```python
from pathbridge.testing.generators import IntegrationTestGenerator

async def generate_integration_tests():
    generator = IntegrationTestGenerator()
    
    # API endpoint testing
    api_tests = await generator.generate_api_tests(
        openapi_spec="api/openapi.yaml",
        test_scenarios=[
            "happy_path",
            "validation_errors", 
            "authentication_failures",
            "rate_limiting"
        ]
    )
    
    # Database integration tests
    db_tests = await generator.generate_database_tests(
        models=["User", "Order", "Product"],
        test_operations=["create", "read", "update", "delete"]
    )
    
    return {
        "api_tests": api_tests,
        "database_tests": db_tests
    }
```

### Acceptance Test Generation

```python
from pathbridge.testing.generators import AcceptanceTestGenerator

async def generate_acceptance_tests():
    generator = AcceptanceTestGenerator()
    
    user_story = {
        "title": "User Login",
        "acceptance_criteria": [
            "Given valid credentials, when user logs in, then they receive a token",
            "Given invalid credentials, when user logs in, then they receive an error"
        ]
    }
    
    # Generate BDD-style tests
    bdd_tests = await generator.generate_bdd_tests(
        user_story=user_story,
        format="gherkin"
    )
    
    return bdd_tests

# Example generated BDD test
"""
Feature: User Authentication
  Scenario: Successful login with valid credentials
    Given a user with username "testuser" and password "validpass"
    When the user attempts to login
    Then the login should be successful
    And a JWT token should be returned
    And the token should be valid for 24 hours
"""
```

## Test Quality Validation

### Mutation Testing

```python
from pathbridge.testing.mutation import MutationTester

async def validate_test_quality():
    mutation_tester = MutationTester()
    
    # Run mutation tests
    result = await mutation_tester.run_mutation_tests(
        source_files=["src/user_service.py"],
        test_files=["tests/test_user_service.py"],
        mutation_operators=["arithmetic", "relational", "logical"]
    )
    
    print(f"Mutation Score: {result.mutation_score}%")
    print(f"Killed Mutants: {result.killed_mutants}")
    print(f"Surviving Mutants: {result.surviving_mutants}")
    
    # Improve tests for surviving mutants
    if result.mutation_score < 80:
        improved_tests = await mutation_tester.generate_tests_for_survivors(
            surviving_mutants=result.surviving_mutants
        )
        return improved_tests
```

### Coverage Analysis

```python
from pathbridge.testing.coverage import CoverageAnalyzer

async def analyze_coverage():
    analyzer = CoverageAnalyzer()
    
    # Run coverage analysis
    coverage_result = await analyzer.analyze_coverage(
        source_files=["src/"],
        test_files=["tests/"],
        coverage_types=["line", "branch", "function"]
    )
    
    print(f"Line Coverage: {coverage_result.line_coverage}%")
    print(f"Branch Coverage: {coverage_result.branch_coverage}%")
    
    # Generate tests for uncovered code
    if coverage_result.line_coverage < 90:
        missing_tests = await analyzer.generate_tests_for_uncovered_lines(
            uncovered_lines=coverage_result.uncovered_lines
        )
        return missing_tests
```

## Framework-Specific Integration

### Python/pytest Integration

```python
# pathbridge/testing/frameworks/pytest_adapter.py
class PytestAdapter:
    def generate_test_file(self, test_cases: List[TestCase]) -> str:
        template = """
import pytest
from unittest.mock import Mock, patch
from src.{module} import {class_name}

class Test{class_name}:
{test_methods}
"""
        
        test_methods = []
        for test_case in test_cases:
            method = f"""
    def test_{test_case.name}(self):
        # Arrange
        {test_case.setup_code}
        
        # Act
        {test_case.execution_code}
        
        # Assert
        {test_case.assertion_code}
"""
            test_methods.append(method)
        
        return template.format(
            module=test_cases[0].module,
            class_name=test_cases[0].target_class,
            test_methods="\n".join(test_methods)
        )
```

### JavaScript/Jest Integration

```javascript
// pathbridge/testing/frameworks/jest_adapter.js
class JestAdapter {
    generateTestFile(testCases) {
        const template = `
const { ${testCases[0].targetClass} } = require('../src/${testCases[0].module}');

describe('${testCases[0].targetClass}', () => {
${testCases.map(tc => this.generateTestMethod(tc)).join('\n')}
});
`;
        return template;
    }
    
    generateTestMethod(testCase) {
        return `
    test('${testCase.name}', async () => {
        // Arrange
        ${testCase.setupCode}
        
        // Act
        ${testCase.executionCode}
        
        // Assert
        ${testCase.assertionCode}
    });`;
    }
}
```

## TDD Workflow Integration

### Red-Green-Refactor Cycle

```python
from pathbridge.testing.tdd import TDDOrchestrator

class TDDWorkflow:
    def __init__(self):
        self.orchestrator = TDDOrchestrator()
    
    async def execute_tdd_cycle(self, user_story: Dict[str, Any]) -> Dict[str, Any]:
        # RED: Generate failing tests first
        failing_tests = await self.orchestrator.generate_failing_tests(
            acceptance_criteria=user_story["acceptance_criteria"],
            business_rules=user_story["business_rules"]
        )
        
        # Verify tests fail
        test_result = await self.orchestrator.run_tests(failing_tests)
        assert not test_result.all_passed, "Tests should fail initially"
        
        # GREEN: Generate minimal implementation
        implementation = await self.orchestrator.generate_minimal_implementation(
            failing_tests=failing_tests,
            target_coverage=90
        )
        
        # Verify tests pass
        test_result = await self.orchestrator.run_tests(failing_tests)
        assert test_result.all_passed, "Tests should pass after implementation"
        
        # REFACTOR: Improve code quality
        refactored_code = await self.orchestrator.refactor_implementation(
            implementation=implementation,
            quality_metrics={"complexity": "low", "maintainability": "high"}
        )
        
        return {
            "tests": failing_tests,
            "implementation": refactored_code,
            "coverage": test_result.coverage_percentage,
            "mutation_score": await self._calculate_mutation_score(failing_tests, refactored_code)
        }
```

## Configuration

### Test Generation Settings

```python
# pathbridge/testing/config.py
TEST_CONFIG = {
    "default_framework": "pytest",
    "coverage_target": 90,
    "mutation_score_target": 80,
    "max_test_cases_per_function": 5,
    "timeout_seconds": 300,
    "parallel_execution": True,
    "generate_mocks": True,
    "include_edge_cases": True,
    "assertion_style": "descriptive"
}
```

### Environment Variables

```bash
# Test Framework Settings
PATH_TEST_FRAMEWORK=pytest
PATH_COVERAGE_TARGET=90
PATH_MUTATION_TARGET=80

# Test Execution
PATH_TEST_TIMEOUT=300
PATH_TEST_PARALLEL=true
PATH_TEST_VERBOSE=false

# Quality Gates
PATH_BLOCK_ON_COVERAGE_FAIL=false
PATH_BLOCK_ON_MUTATION_FAIL=false
```

## Error Handling

```python
from pathbridge.exceptions import TestGenerationError, CoverageError

async def robust_test_generation():
    try:
        generator = TestGenerator()
        
        result = await generator.generate_test_suite(
            TestRequest(source_file="complex_module.py")
        )
        
        return result
        
    except TestGenerationError as e:
        print(f"Test generation failed: {e}")
        # Fallback to template-based generation
        
    except CoverageError as e:
        print(f"Coverage analysis failed: {e}")
        # Continue without coverage validation
```

## Testing the Testing System

```python
import pytest
from pathbridge.testing.test_generator import TestGenerator

@pytest.mark.asyncio
async def test_test_generator():
    """Meta-test: Test the test generator itself"""
    generator = TestGenerator()
    
    # Simple function to test
    source_code = """
def add(a, b):
    return a + b
"""
    
    # Generate tests
    result = await generator.generate_unit_tests(
        source_code=source_code,
        target_coverage=90
    )
    
    # Validate generated tests
    assert len(result.test_cases) >= 3  # Normal, edge cases, errors
    assert any("add(2, 3)" in tc.code for tc in result.test_cases)
    assert any("assert" in tc.code for tc in result.test_cases)
```

## Best Practices

### Test Quality Guidelines

1. **Meaningful Assertions**: Generate tests with behavioral assertions, not just return value checks
2. **Edge Case Coverage**: Include boundary values, null inputs, and error conditions
3. **Test Independence**: Each test should be isolated and not depend on others
4. **Descriptive Names**: Generate test names that explain the scenario being tested
5. **Proper Setup/Teardown**: Include necessary setup and cleanup code

### Performance Optimization

```python
# Parallel test generation
async def parallel_test_generation():
    generator = TestGenerator()
    
    # Generate tests for multiple files concurrently
    tasks = [
        generator.generate_unit_tests(f"src/module_{i}.py")
        for i in range(10)
    ]
    
    results = await asyncio.gather(*tasks)
    return results
```