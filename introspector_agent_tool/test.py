import openai
import logging
from llama_index.agent import OpenAIAgent
from base import PlaygroundsSubgraphInspectorToolSpec

def inspect_subgraph(
    openai_api_key: str,
    playgrounds_api_key: str,
    identifier: str,
    use_deployment_id: bool,
    user_prompt: str,
):
    """
    Introspect a subgraph using OpenAIAgent and Playgrounds API with the provided parameters.
    
    Args:
        openai_api_key (str): API key for OpenAI.
        playgrounds_api_key (str): API key for Playgrounds.
        identifier (str): Identifier for the subgraph or deployment.
        use_deployment_id (bool): If True, uses deployment ID in the URL.
        user_prompt (str): User's question or prompt for the agent.
        
    Returns:
        str: Agent's response.
    """
    # Set the OpenAI API key
    openai.api_key = openai_api_key
    
    # Initialize the inspector with the provided parameters
    inspector_spec = PlaygroundsSubgraphInspectorToolSpec(
        identifier=identifier, 
        api_key=playgrounds_api_key, 
        use_deployment_id=use_deployment_id,
    )
    
    # Integrate the tool with the agent
    agent = OpenAIAgent.from_tools(inspector_spec.to_tool_list())
    
    # Send the user prompt to the agent
    response = agent.chat(user_prompt)
    return response


if __name__ == "__main__":
    query = inspect_subgraph(
        openai_api_key='YOUR_OPENAI_API_KEY',
        playgrounds_api_key="YOUR_PLAYGROUNDS_API_KEY"",
        identifier="YOUR_SUBGRAPH_OR_DEPLOYMENT_IDENTIFIER",
        use_deployment_id=False,
        user_prompt='Which entities will help me understand the usage of Uniswap V3',
    )
    print(query)
