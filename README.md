# PlaygroundsSubgraphConnector

Playgrounds API is a service provided by [Playgrounds Analytics](https://playgrounds.network) that facilitates interfacing with decentralized subgraphs (indexed blockchain datasets).

The `PlaygroundsSubgraphConnector` is a Python tool designed for LLM agents to seamlessly interface with and query subgraphs on The Graph's decentralized network via the Playgrounds API.

This tool is particularly designed to be used in conjunction with platforms like [Llama index](https://github.com/jerryjliu/llama_index) or [langchain](https://python.langchain.com/docs/modules/agents/tools/custom_tools).

## Key Features:
- **Direct access to Decentralized Subgraphs (Datasets)**: No need for wallet or GRT management. Access a vast range of blockchain datasets directly.
- **LLM x Blockchain data**: Develop AI applications that leverage blockchain data effortlessly with the integrated tool.

## Resources:
- **Playgrounds Analytics**: To learn more about the Playgrounds API, visit the [official website](https://playgrounds.network/).
- **Playgrounds API Key**: Obtain your Playgrounds API Key and get started for free [here](https://app.playgrounds.network/signup).
- **OpenAI Key**: Obtain your API key from OpenAI: https://platform.openai.com/
- **Subgraphs**: Discover and choose from a variety of Subgraphs (datasets) available on [The Graph's Explorer](https://thegraph.com/explorer).

## How to Use:

1. **Initialization**: Begin by initializing the tool with the necessary `identifier` (either the Subgraph ID or Deployment ID) and your `api_key`.
    ```python
    connector_spec = PlaygroundsSubgraphConnectorToolSpec(
        identifier="YOUR_SUBGRAPH_OR_DEPLOYMENT_IDENTIFIER", 
        api_key="YOUR_PLAYGROUNDS_API_KEY"
    )
    ```

2. **Optional Parameters**:
   - `use_deployment_id`: Specify if you're using a deployment ID instead of a subgraph ID. Defaults to `False`.

3. **Querying**: Use the initialized tool to make queries and obtain blockchain data.
    ```python
    response = prompt_to_data(
        prompt="Your query here...",
        openai_key="YOUR_OPENAI_API_KEY",
        identifier="YOUR_SUBGRAPH_OR_DEPLOYMENT_IDENTIFIER",
        pg_key="YOUR_PLAYGROUNDS_API_KEY"
    )
    ```

## Basic Example - See Notebook for full examples

```python
import openai
from llama_index.agent import OpenAIAgent
from base import PlaygroundsSubgraphConnectorToolSpec

def prompt_to_data(prompt, openai_key, identifier, pg_key, use_deployment_id=False):
    """
    Query any decentralized subgraph using OpenAIAgent and Playgrounds API.
    
    Args:
        prompt (str): The query text to be used for the GraphQL request.
        openai_key (str): The API key for OpenAI.
        identifier (str): The identifier for the subgraph or deployment.
        pg_key (str): The API key for Playgrounds.
        use_deployment_id (bool, optional): Flag to use deployment id in the URL. Defaults to False.
        
    Returns:
        str: Agent's response.
    """
    
    # Set the OpenAI API key
    openai.api_key = openai_key
    
    # Initialize the tool specification with appropriate logging and pagination settings
    connector_spec = PlaygroundsSubgraphConnectorToolSpec(
        identifier=identifier, 
        api_key=pg_key,
        use_deployment_id=use_deployment_id,
    )
    
    # Setup agent with the tool
    agent = OpenAIAgent.from_tools(connector_spec.to_tool_list())
    
    # Make a query using the agent
    response = agent.chat(prompt)
    return response

if __name__ == "__main__":
    response = prompt_to_data(
        prompt="query the financialsDailySnapshots for id, timestamp, totalValueLockedUSD, and dailyVolumeUSD. only give me the first 2 rows",
        openai_key="YOUR_OPENAI_API_KEY",
        identifier="YOUR_SUBGRAPH_OR_DEPLOYMENT_IDENTIFIER",
        pg_key="YOUR_PLAYGROUNDS_API_KEY"
    )
    print(response)
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) 
and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. 


# PlaygroundsSubgraphIntrospector

The `PlaygroundsSubgraphIntrospectorToolSpec` is a tool designed for LLM agents to introspect and gain insights into the schema of subgraphs on The Graph's decentralized network via the Playgrounds API.

Similar to `PlaygroundsSubgraphConnectorToolSpec`, This tool is for use with LLM development frameworks like [Llama index](https://github.com/jerryjliu/llama_index) or [langchain](https://python.langchain.com/docs/modules/agents/tools/custom_tools).

## Key Features:
- **Introspection of Decentralized Subgraphs (Datasets)**: Easily understand and explore the schema of any subgraph.
- **LLM x Blockchain Data**: Develop AI applications that harness introspective insights from blockchain data effortlessly.

## Resources:
- **Playgrounds Analytics**: To learn more about the Playgrounds API, delve into the [official website](https://playgrounds.network/).
- **Playgrounds API Key**: Obtain your Playgrounds API Key and embark on your journey for free [here](https://app.playgrounds.network/signup).
- **OpenAI Key**: Obtain your API key from OpenAI: https://platform.openai.com/
- **Subgraphs**: Discover and select from a variety of Subgraphs (datasets) on [The Graph's Explorer](https://thegraph.com/explorer).

## How to Use:

1. **Initialization**: Initialize the introspector tool with the required `identifier` (either the Subgraph ID or Deployment ID), `api_key`, and specify if you're using a deployment ID.
    ```python
    introspector_spec = PlaygroundsSubgraphIntrospectorToolSpec(
        identifier="YOUR_SUBGRAPH_OR_DEPLOYMENT_IDENTIFIER", 
        api_key="YOUR_PLAYGROUNDS_API_KEY", 
        use_deployment_id=False  # True if using Deployment ID
    )
    ```

2. **Introspection**: With the initialized tool, perform introspection on the subgraph's schema.
    ```python
    response = inspect_subgraph(
        openai_api_key='YOUR_OPENAI_API_KEY',
        playgrounds_api_key="YOUR_PLAYGROUNDS_API_KEY",
        identifier="YOUR_SUBGRAPH_OR_DEPLOYMENT_IDENTIFIER",
        use_deployment_id=False,
        user_prompt='Which entities will help me understand the usage of Uniswap V3?'
    )
    ```

3. **Output**: The result provides a deeper understanding of the subgraph's schema, aiding in subsequent data queries and analysis.

## Basic Example - See Notebook for full examples

```python
import openai
from llama_index.agent import OpenAIAgent
from base import PlaygroundsSubgraphIntrospectorToolSpec

def inspect_subgraph(prompt, openai_key, identifier, pg_key, use_deployment_id=False):
    """
    Introspect a subgraph schema using OpenAIAgent and Playgrounds API based on the provided parameters.
    
    Args:
        prompt (str): The user's question or prompt for the agent.
        openai_key (str): API key for OpenAI.
        identifier (str): Identifier for the subgraph or deployment.
        pg_key (str): API key for Playgrounds.
        use_deployment_id (bool, optional): If True, uses deployment ID in the URL. Defaults to False.
        
    Returns:
        str: Agent's response.
    """
    # Set the OpenAI API key
    openai.api_key = openai_key
    
    # Initialize the introspector tool specification with the subgraph's identifier and the Playgrounds API key
    introspector_spec = PlaygroundsSubgraphIntrospectorToolSpec(
        identifier=identifier, 
        api_key=pg_key, 
        use_deployment_id=use_deployment_id,
    )
    
    # Integrate the introspector tool with the agent
    agent = OpenAIAgent.from_tools(introspector_spec.to_tool_list())
    
    # Make an introspection query using the agent
    response = agent.chat(prompt)
    return response

if __name__ == "__main__":

    # Run the introspection function and print the result
    result = inspect_subgraph(
        prompt="Which entities will guide me in comprehending the usage of Uniswap V3?",
        openai_key='YOUR_OPENAI_API_KEY',
        identifier="YOUR_SUBGRAPH_OR_DEPLOYMENT_IDENTIFIER",
        pg_key="YOUR_PLAYGROUNDS_API_KEY",
        use_deployment_id=False,
    )
    print(result)
```

This loader is designed to be used as a way to load data into [LlamaIndex](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) 
and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent. 
