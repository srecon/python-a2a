from python_a2a import AgentNetwork, A2AClient, AIAgentRouter


from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
import os

# Create an agent network
network = AgentNetwork(name="Travel Assistant Network")

# Add agents to the network
network.add("weather", "http://localhost:8001")
network.add("Sites", "http://localhost:8002")

# List all available agents
print("\nAvailable Agents:")
for agent_info in network.list_agents():
    print(f"- {agent_info['name']}: {agent_info['description']}")


# Create a router to intelligently direct queries to the best agent
llm_client=A2AClient("http://localhost:5001")

router = AIAgentRouter(
    llm_client=llm_client,  # LLM for making routing decisions
    agent_network=network
)

# Route a query to the appropriate agent
agent_name, confidence = router.route_query("What's the weather like in Paris?")
print(f"Routing to {agent_name} with {confidence:.2f} confidence")

# Get the selected agent and ask the question
agent = network.get_agent(agent_name)
response = agent.ask("What's the weather like in Paris?")
print(f"Response: {response}")


#template = "You are a helpful travel guide.\n\nQuestion: {query}\n\nAnswer:"
#prompt = PromptTemplate.from_template(template)

# Make summary of the plan
prompt = f"You are a travel assistant. Depended on the weather forecast {response}, suggest me a few must-see attractions"
print(f"Response: {prompt}")

llm_result = llm_client.ask(prompt)

print(f"LLM response: {llm_result}")
#travel_result = travel_client.ask('{"query": "What are some must-see attractions in Bangladesh?"}')

