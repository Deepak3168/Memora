from models.relations  import HAS_CATEGORY
from models.category import CategoryNode
import secrets


from models.relations import HAS_CATEGORY
from models.category import CategoryNode
import secrets
from datetime import datetime


def create_and_connect_categories(user):
    """
    Helper function to create multiple default categories
    and connect them to a user using HAS_CATEGORY relation.
    """

    categories_data = [
        {
            "name": "Skills",
            "description": "A node that defines skills. All skill-related nodes belong here.",
            "tags": ["Skill", "Hands-on Experience"],
            "remarks": "User abilities and things they are good at."
        },
        {
            "name": "Interests",
            "description": "Things the user is curious about or follows.",
            "tags": ["Interest", "Hobby"],
            "remarks": "Topics or areas the user likes or wants to explore."
        },
        {
            "name": "Profession",
            "description": "Professional identity and work background.",
            "tags": ["Work", "Career"],
            "remarks": "User’s job role, industry, or career direction."
        },
        {
            "name": "Projects",
            "description": "Past or ongoing projects by the user.",
            "tags": ["Project", "Work", "Build"],
            "remarks": "Things the user has built, contributed to, or is planning."
        },
        {
            "name": "Tools/Technologies",
            "description": "Technologies and tools the user uses.",
            "tags": ["Tech", "Tools", "Software"],
            "remarks": "Specific tools or technologies the user is familiar with."
        },
        {
            "name": "Knowledge",
            "description": "Accumulated knowledge or domain understanding.",
            "tags": ["Knowledge", "Concepts"],
            "remarks": "Concepts, theories, or topics the user has learned."
        },
        {
            "name": "Personal Notes",
            "description": "Notes added by the user for memory purposes.",
            "tags": ["Notes", "Personal"],
            "remarks": "Small personal references or quick thoughts from the user."
        },
        {
            "name": "Tasks/Todo",
            "description": "User tasks and todo items.",
            "tags": ["Task", "Todo", "Work"],
            "remarks": "Things the user needs to complete."
        },
    ]

    created_categories = []

    # Create and connect each category
    for c in categories_data:
        node = CategoryNode(
            id=str(secrets.randbits(64)),
            name=c["name"],
            description=c["description"],
            tags=c["tags"],
            remarks=c["remarks"],
            created_at=datetime.utcnow()
        )

        saved = node.create()

        relation = HAS_CATEGORY(
            source=user,
            target=saved
        )
        relation.merge()

        created_categories.append(saved)

    return created_categories


    


