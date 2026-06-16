# server.py
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("WeatherService")

@mcp.tool()
def get_weather(city: str) -> str:
    """
    Fetches the current weather for a given city.
    """
    # In a real app, you'd call an API here
    if city.lower() == "new york":
        return "It is 22°C and sunny in New York."
    else:
        return f"It is 15°C and cloudy in {city}."

if __name__ == "__main__":
    mcp.run()
