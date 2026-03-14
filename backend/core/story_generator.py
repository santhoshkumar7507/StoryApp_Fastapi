from sqlalchemy.orm import Session

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.prompts import STORY_PROMPT
from models.story import Story, StoryNode
from core.models import StoryLLMResponse, StoryNodeLLM, StoryOptionLLM
from dotenv import load_dotenv
import os

load_dotenv()

class StoryGenerator:

    @classmethod
    def _get_llm(cls):
        openai_api_key = os.getenv("CHOREO_OPENAI_CONNECTION_OPENAI_API_KEY")
        serviceurl = os.getenv("CHOREO_OPENAI_CONNECTION_SERVICEURL")

        if openai_api_key and serviceurl:
            return ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key, base_url=serviceurl)

        return ChatOpenAI(model="gpt-4o-mini")

    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy")-> Story:
        # Mock an impressive interactive story instead of using OpenAI to avoid billing issues
        import random
        # Create a dynamic mock story based on the theme
        def create_ending(content, winning):
            return StoryNodeLLM(content=content, isEnding=True, isWinningEnding=winning, options=[])
            
        def create_node(content, *options):
            opts = []
            for text, next_node in options:
                opts.append(StoryOptionLLM(text=text, nextNode=next_node.model_dump()))
            return StoryNodeLLM(content=content, isEnding=False, isWinningEnding=False, options=opts)

        story_title = f"The Epic of {theme.title()}"
        
        # Branch 1: The direct approach
        bad_end_1 = create_ending(f"You charged forward blindly. The challenges of the {theme} world were too much. You have failed.", False)
        good_end_1 = create_ending(f"Your courage paid off! You discovered the hidden secrets of the {theme} realm and emerged victorious!", True)
        mid_node_1 = create_node(f"You encounter the Guardian of the {theme}. It demands a tribute.", 
                                 ("Fight the Guardian", bad_end_1), 
                                 ("Offer a peaceful tribute", good_end_1))
                                 
        # Branch 2: The stealth approach
        bad_end_2 = create_ending(f"Your footsteps echoed in the silent {theme} caverns. You were caught!", False)
        good_end_2 = create_ending(f"You slipped past all the dangers. The treasure of the {theme} is now yours!", True)
        mid_node_2 = create_node(f"You find a hidden, narrow path. It looks dark and dangerous, but smells like {theme} magic.", 
                                 ("Run through quickly", bad_end_2), 
                                 ("Walk slowly and carefully", good_end_2))

        # Root Node
        root_node = create_node(f"You awaken in a mysterious place surrounded by a mystical aura of {theme}. Two paths lie before you.", 
                                ("Take the brightly lit path", mid_node_1), 
                                ("Take the dark, hidden path", mid_node_2))

        story_structure = StoryLLMResponse(title=story_title, rootNode=root_node)

        story_db = Story(title=story_structure.title, session_id=session_id)
        db.add(story_db)
        db.flush()

        root_node_data = story_structure.rootNode
        if isinstance(root_node_data, dict):
            root_node_data = StoryNodeLLM.model_validate(root_node_data)

        cls._process_story_node(db, story_db.id, root_node_data, is_root=True)

        db.commit()
        return story_db

    @classmethod
    def _process_story_node(cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool = False) -> StoryNode:
        node = StoryNode(
            story_id=story_id,
            content=node_data.content if hasattr(node_data, "content") else node_data["content"],
            is_root=is_root,
            is_ending=node_data.isEnding if hasattr(node_data, "isEnding") else node_data["isEnding"],
            is_winning_ending=node_data.isWinningEnding if hasattr(node_data, "isWinningEnding") else node_data["isWinningEnding"],
            options=[]
        )
        db.add(node)
        db.flush()

        if not node.is_ending and (hasattr(node_data, "options") and node_data.options):
            options_list = []
            for option_data in node_data.options:
                next_node = option_data.nextNode

                if isinstance(next_node, dict):
                    next_node = StoryNodeLLM.model_validate(next_node)

                child_node = cls._process_story_node(db, story_id, next_node, False)

                options_list.append({
                    "text": option_data.text,
                    "node_id": child_node.id
                })

            node.options = options_list

        db.flush()
        return node