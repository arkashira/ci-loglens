# CI LogLens

CI LogLens is a Python project that connects to various CI tools and analyzes logs.

## Usage

1. Create a `LogLensConfig` object with the desired CI tool and configuration.
2. Create a `LogLens` object with the `LogLensConfig` object.
3. Call the `connect_ci_tool` method to connect to the CI tool.
4. Call the `analyze_ci_logs` method to analyze the logs.

## Testing

Run the tests using `pytest`:
