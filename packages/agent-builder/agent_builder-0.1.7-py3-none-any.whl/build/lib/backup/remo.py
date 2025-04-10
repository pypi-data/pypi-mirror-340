from pydantic import BaseModel, Field
from agent_builder.builders.tool_builder import ToolBuilder

# Define your schema as a subclass of BaseModel
class GetTemperatureSchema(BaseModel):
    city: str = Field(description="City for which temperature has to be checked.")

# Example function to use with the tool
def get_temperature(city: str) -> float:
    return 30.1


# Creating the tool

# Instantiate the tool builder.
tool_builder = ToolBuilder()
# Define name of tool.
tool_builder.set_name(name="get-temparature-tool")
# Set the function for the tool.
tool_builder.set_function(function=get_temperature)
# Provide the description for tool
tool_builder.set_description(description="Tool to get temperature of given city")
# Add the tool schema
tool_builder.set_schema(schema=GetTemperatureSchema)
# Build and get the tool
get_temperature_tool = tool_builder.build()


from agent_builder.builders.agent_builder import AgentBuilder
from langchain_openai import ChatOpenAI

# Initialize LLM (Large Language Model)
llm = ChatOpenAI(
    model="gpt-4o", 
    api_key="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",
    base_url="https://api.openai.com/v1"
)

# Create an agent
agent_builder = AgentBuilder()
agent_builder.set_goal(
    """You are customer service respresentative at weather forecast agency. 
    Your duty is to help user with query related to forecast."""
)
agent_builder.set_llm(llm)

agent_builder.add_tool(get_temperature_tool)
agent = agent_builder.build()



if __name__ == "__main__":
    # Now the agent can invoke the tool
    response = agent.invoke(input="Hi, what is current temperature of Pune", chat_history=[])
    print(response)