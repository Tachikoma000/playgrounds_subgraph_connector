import openai
from llama_index.agent import OpenAIAgent
from base import PlaygroundsSubgraphConnectorToolSpec

"""
SIMPLE TEST 
"""

def simple_test():
    """
    Run a simple test querying the financialsDailySnapshots from Uniswap V3 subgraph using OpenAIAgent and Playgrounds API.
    """
    # Set the OpenAI API key
    openai.api_key = 'YOUR_OPENAI_API_KEY'
    
    # Initialize the tool specification
    connector_spec = PlaygroundsSubgraphConnector(
        identifier="YOUR_SUBGRAPH_OR_DEPLOYMENT_IDENTIFIER", 
        api_key="YOUR_PLAYGROUNDS_API_KEY", 
        use_deployment_id=False
    )
    
    # Setup agent with the tool
    agent = OpenAIAgent.from_tools(connector_spec.to_tool_list())
    
    # Make a query using the agent
    response = agent.chat(
        'query the financialsDailySnapshots for id, timestamp, totalValueLockedUSD, and dailyVolumeUSD. only give me the first 2 rows'
    )
    print(response)

if __name__ == "__main__":
    simple_test()

