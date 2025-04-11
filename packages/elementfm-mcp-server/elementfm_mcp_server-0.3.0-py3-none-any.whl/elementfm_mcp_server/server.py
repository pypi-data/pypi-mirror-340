# server.py
from mcp.server.fastmcp import FastMCP
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import os
import requests
import sys

# Set default frontend URL
global FRONTEND_ROOT_URL
FRONTEND_ROOT_URL = os.getenv('FRONTEND_ROOT_URL', 'https://app.element.fm')

# Create an MCP server
mcp = FastMCP("elementfm-mcp-server")

# Pydantic models for request/response types
class Category(BaseModel):
    id: int
    category_name: str
    subcategory_name: Optional[str] = None

class ShowCategory(BaseModel):
    id: str
    category_name: str
    subcategory_name: Optional[str] = None

class Workspace(BaseModel):
    id: str
    name: str
    show_count: Optional[int] = None

class Show(BaseModel):
    id: str
    name: str
    author: Optional[str] = None
    description: Optional[str] = None
    explicit: Optional[bool] = None
    link: Optional[str] = None
    language: Optional[str] = None
    copyright: Optional[str] = None
    funding_url: Optional[str] = None
    funding_text: Optional[str] = None
    email: Optional[str] = None
    category: List[ShowCategory] = []

class Episode(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    show_id: str
    publish_status: Optional[str] = None
    episode_number: int
    season_number: int

class Invitation(BaseModel):
    id: str
    email: str
    accepted: bool
    workspace_id: str

# Workspace endpoints
@mcp.tool()
def list_workspaces() -> List[Workspace]:
    """List all workspaces"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    
    try:
        # Make request to frontend API
        response = requests.get(
            f"{FRONTEND_ROOT_URL}/api/workspaces",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        response.raise_for_status()
        
        # Convert response data to list of Workspace objects
        workspaces_data = response.json()
        return [Workspace(
            id=workspace['workspace']['id'],
            name=workspace['workspace']['name'],
            show_count=workspace.get('show_count')
        ) for workspace in workspaces_data]
    except Exception as e:
        print(f"Error listing workspaces: {e}")
        raise e


@mcp.tool()
def create_workspace(name: str) -> Workspace:
    """Create a new workspace"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")

    response = requests.post(
        f"{FRONTEND_ROOT_URL}/api/workspaces",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"name": name}
    )
    response.raise_for_status()
    
    # Convert response data to Workspace object
    workspace_data = response.json()
    return Workspace(**workspace_data)

# Show endpoints
@mcp.tool()
def list_shows(workspace_id: str) -> List[Show]:
    """List all shows"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    
    # Make request to frontend API
    response = requests.get(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/shows",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()

    # Convert response data to list of Show objects
    shows_data = response.json()
    return [Show(**show) for show in shows_data['shows']]

@mcp.tool()
def create_show(workspace_id: str, name: str) -> Show:
    """Create a new show"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.post(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/shows",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"name": name}
    )
    response.raise_for_status()

    # Convert response data to Show object
    show_data = response.json()
    return Show(**show_data)

@mcp.tool()
def update_show(
    workspace_id: str,
    show_id: str,
    name: str, 
    description: str,
    author: str,
    link: str,
    language: str,
    copyright: str,
    category_id: int,
    funding_url: str,
    funding_text: str,
    email: str,
    explicit: bool) -> Show:
    """Update a show"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.patch(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/shows/{show_id}",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "name": name,
            "author": author, 
            "description": description,
            "explicit": explicit,
            "link": link,
            "language": language, 
            "copyright": copyright,
            "category": category_id,
            "funding_url": funding_url,
            "funding_text": funding_text,
            "email": email
        }
    )
    response.raise_for_status()
    
    # Convert response data to Show object
    show_data = response.json()
    return Show(**show_data["updated"])

@mcp.tool()
def upload_show_image(workspace_id: str, show_id: str, image_url: str) -> str:
    """Upload a show image artwork"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set") 
    
    # Download the image file from the URL
    response = requests.get(image_url)
    response.raise_for_status()
    image_file = response.content
    image_file_name = f"{show_id}"
    image_file_path = os.path.join(os.getcwd(), image_file_name)
    with open(image_file_path, "wb") as f:
        f.write(image_file)

    # Make request to frontend API
    response = requests.post(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/shows/{show_id}/artwork", 
        headers={"Authorization": f"Bearer {api_key}"},
        files={"image": open(image_file_path, "rb")}
    )
    print(f"Response: {response.json()}", flush=True)
    print(f"Response status: {response.status_code}", flush=True)

    # Delete the image file
    print(f"Deleting image file {image_file_path}", flush=True)
    os.remove(image_file_path)

    response.raise_for_status()
    
    return response.json()["message"]

# Episode endpoints
@mcp.tool()
def list_episodes(workspace_id: str, show_id: str) -> List[Episode]:
    """List all episodes for a show"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.get(
            f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/shows/{show_id}/episodes",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()
    
    # Convert response data to list of Episode objects
    episodes_data = response.json()
    return [Episode(**episode) for episode in episodes_data["episodes"]]

@mcp.tool()
def create_episode(workspace_id: str, show_id: str, title: str, 
                  season_number: int, episode_number: int) -> Episode:
    """Create a new episode"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.post(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/shows/{show_id}/episodes",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "title": title,
            "season_number": season_number,
            "episode_number": episode_number
            }
    )
    response.raise_for_status()
    
    # Convert response data to Episode object
    episode_data = response.json()
    return Episode(**episode_data)

@mcp.tool()
def upload_episode_audio(workspace_id: str, show_id: str, episode_id: str, audio_url: str) -> str:
    """Upload an episode audio file"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    
    # Download the audio file from the URL
    response = requests.get(audio_url)
    response.raise_for_status()
    audio_file = response.content
    audio_file_name = f"{episode_id}.mp3"
    audio_file_path = os.path.join(os.getcwd(), audio_file_name)
    print(f"Saving audio file to {audio_file_path}", flush=True)
    with open(audio_file_path, "wb") as f:
        f.write(audio_file)

    # Make request to frontend API
    response = requests.post(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/shows/{show_id}/episodes/{episode_id}/audio",
        headers={"Authorization": f"Bearer {api_key}"},
        files={"audio": open(audio_file_path, "rb")}
    )
    print(f"Response: {response.json()}", flush=True)
    print(f"Response status: {response.status_code}", flush=True)

    # Delete the audio file
    print(f"Deleting audio file {audio_file_path}", flush=True)
    os.remove(audio_file_path)
    
    response.raise_for_status()
    return response.json()["message"]

@mcp.tool()
def update_episode(workspace_id: str, show_id: str, episode_id: str, title: str,
                  description: str) -> Episode:
    """Update an episode"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.patch(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/shows/{show_id}/episodes/{episode_id}",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"title": title, "description": description}
    )
    response.raise_for_status()
    
    # Convert response data to Episode object
    episode_data = response.json()
    return Episode(**episode_data)

@mcp.tool()
def publish_episode(workspace_id: str, show_id: str, episode_id: str) -> Dict[str, Any]:
    """Publish an episode"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.post(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/shows/{show_id}/episodes/{episode_id}/publish",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()
    return response.json()["updated_episode"]

# AI features
@mcp.tool()
def transcribe_audio(workspace_id: str, show_id: str, episode_id: str) -> Dict[str, Any]:
    """Transcribe audio for an episode"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.post(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/shows/{show_id}/episodes/{episode_id}/transcribe",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()
    return response.json()

@mcp.tool()
def generate_ai_chapters(workspace_id: str, show_id: str, episode_id: str) -> Dict[str, Any]:
    """Generate AI chapters for an episode"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.post(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/shows/{show_id}/episodes/{episode_id}/autochapter",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()
    
    return response.json()

@mcp.tool()
def generate_ai_show_notes(workspace_id: str, show_id: str, episode_id: str) -> Dict[str, Any]:
    """Generate AI show notes for an episode"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.post(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/shows/{show_id}/episodes/{episode_id}/summarize",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()
    
    # Convert response data to Episode object
    return response.json()

# Workspace invitation endpoints
@mcp.tool()
def list_invitations() -> List[Invitation]:
    """List workspace invitations"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.get(
        f"{FRONTEND_ROOT_URL}/api/workspaces/invitations",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()
    
    # Convert response data to list of invitations
    invitations_data = response.json()
    return [Invitation(**invitation) for invitation in invitations_data]

@mcp.tool()
def send_workspace_invite(workspace_id: str, invitee_email: str) -> Dict[str, Any]:
    """Send a workspace invitation"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    # Make request to frontend API
    response = requests.post(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/invite",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"invitee_email": invitee_email}
    )
    response.raise_for_status()
    
    # Convert response data to invitation object
    return response.json()


@mcp.tool()
def search_workspace(workspace_id: str, query: str) -> Dict[str, Any]:
    """Search within a workspace"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")
    
    # Make request to frontend API
    response = requests.get(
        f"{FRONTEND_ROOT_URL}/api/workspaces/{workspace_id}/search",
        headers={"Authorization": f"Bearer {api_key}"},
        params={"q": query}
    )
    response.raise_for_status()
    
    # Return search results
    return response.json()

@mcp.tool()
def list_categories() -> List[Category]:
    """List show categories"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY environment variable is not set")

    # Make request to frontend API
    response = requests.get(
        f"{FRONTEND_ROOT_URL}/api/categories",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()

    # Convert response data to list of categories
    categories_data = response.json()
    return [Category(**category) for category in categories_data]


def main():
    """Entry point for the MCP server"""
    if not os.getenv('API_KEY'):
        print("API_KEY environment variable is not set")
        sys.exit(1)
    if not FRONTEND_ROOT_URL:
        print("FRONTEND_ROOT_URL environment variable is not set")
        sys.exit(1)

    t = sys.argv[1] if len(sys.argv) > 1 else "stdio"
    if t not in ["stdio", "sse"]:
        t = "stdio"
    print(f"Running MCP server with transport: {t}")
    print(f"Frontend root URL: {FRONTEND_ROOT_URL}")
    mcp.run(transport=t)

if __name__ == "__main__":
    main()