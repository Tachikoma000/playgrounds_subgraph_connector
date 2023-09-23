import openai
from llama_index.agent import OpenAIAgent
# from llama_hub.tools.playgrounds_subgraph_introspector.base import PlaygroundsSubgraphIntrospectorToolSpec
from base import PlaygroundsSubgraphIntrospectorToolSpec

def simple_test():
    """
    Run a simple test introspecting the Uniswap V3 subgraph schema using OpenAIAgent and Playgrounds API.
    """
    # Set the OpenAI API key
    openai.api_key = 'YOUR_OPENAI_API_KEY'
    
    # Initialize the tool specification with the subgraph's identifier and the Playgrounds API key
    introspector_spec = PlaygroundsSubgraphIntrospectorToolSpec(
        identifier="YOUR_SUBGRAPH_OR_DEPLOYMENT_IDENTIFIER", 
        api_key="YOUR_PLAYGROUNDS_API_KEY", 
        use_deployment_id=False  # Set to True if using Deployment ID
    )
    
    # Setup agent with the tool
    agent = OpenAIAgent.from_tools(introspector_spec.to_tool_list())
    
    # Make an introspection query using the agent
    response = agent.chat(
        'which fields will help me understand the usage of the protocol'
    )
    print(response)

if __name__ == "__main__":
    simple_test()
