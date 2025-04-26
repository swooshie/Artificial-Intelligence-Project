import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class ReActAgent:
    def __init__(self, domain_file: str, problem_file: str):
        self.domain_file = domain_file
        self.problem_file = problem_file

    async def act(self, session: ClientSession):
        # Step 1: Retrieve the latest environment information.
        env_resp = await session.call_tool("get_env_info", {})
        # The response structure (from our MCP server) contains our data.
        env_info = env_resp.content[0].data
        print("[Agent] Retrieved environment info:", env_info)

        # Step 2: Read the domain and problem files from disk.
        with open(self.domain_file, "r") as f:
            domain_content = f.read()
        with open(self.problem_file, "r") as f:
            problem_content = f.read()

        # Optionally modify the problem based on dynamic pricing.
        if env_info.get("dynamic_pricing", False):
            print("[Agent] Dynamic pricing active; modifying problem if needed.")
            # Here you could add modifications; here we leave it unchanged.
            modified_problem = problem_content
        else:
            modified_problem = problem_content

        # Step 3: Call the planning tool via MCP.
        planning_resp = await session.call_tool("planning_call", {
            "domain": domain_content,
            "problem": modified_problem
        })
        plan = planning_resp.content[0].data.get("plan")
        print("[Agent] Plan generated:", plan)

        # Step 4: Execute the plan step-by-step.
        for action in plan:
            print("[Agent] Executing action:", action)
            exec_resp = await session.call_tool("execute_action", {"action": action})
            print("[Agent] Action execution response:", exec_resp.content[0].data)
            # Pause briefly between actions to simulate observation feedback.
            await asyncio.sleep(1)
        print("[Agent] Plan execution complete.")
        return plan

async def main():
    # Define parameters for the MCP client.
    # NOTE: Adjust 'command' and 'args' as needed to start your MCP server.
    server_params = StdioServerParameters(
        command="uv", args=["run", "mcp_server.py", "server"], env=os.environ
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            # Instantiate and run the ReAct agent.
            agent = ReActAgent("domain.pddl", "problem.pddl")
            await agent.act(session)

if __name__ == "__main__":
    asyncio.run(main())
