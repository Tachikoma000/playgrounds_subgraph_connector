import openai
import logging
from llama_index.agent import OpenAIAgent
from base import PlaygroundsSubgraphConnectorToolSpec

logging.basicConfig(level=logging.DEBUG)

"""
SIMPLE TEST 
"""

def simple_test():
    """
    Run a simple test querying the financialsDailySnapshots from Uniswap V3 subgraph using OpenAIAgent and Playgrounds API.
    """
    # Set the OpenAI API key
    openai.api_key = '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'
    
    # Initialize the tool specification
    connector_spec = PlaygroundsSubgraphConnectorToolSpec(
        identifier="ELUcwgpm14LKPLrBRuVvPvNKHQ9HvwmtKgKSH6123cr7", 
        api_key="pg-AqAFS8G3TN3Kagdgw2MrGjFvDGUgxImS", 
        use_deployment_id=False,
        log_level=logging.DEBUG,
        paginate=False
    )
    
    # Setup agent with the tool
    agent = OpenAIAgent.from_tools(connector_spec.to_tool_list())
    
    # Make a query using the agent
    response = agent.chat(
        """ 
        query($last_id: ID) {
            financialsDailySnapshots(first: 2) {
                id
                timestamp
                totalValueLockedUSD
            }
            }
        """
    )
    print(response)

if __name__ == "__main__":
    simple_test()
