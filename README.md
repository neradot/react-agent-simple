# react-simple

A simple ReAct agent code designed for tutorial purposes. This project demonstrates how to create a reactive agent using OpenAI's API and custom tools.

## Setup

### Prerequisites

- Python 3.10 or higher
- Poetry for dependency management

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/neradot/react-simple.git
   cd react-simple
   ```

2. **Install dependencies**:
   Ensure you have Poetry installed, then run:
   ```bash
   poetry install
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```plaintext
   OPENAI_API_KEY=your_openai_api_key
   ```

### Running the Agent
To run the agent, execute the following command:
```bash
poetry run python react.py
```
