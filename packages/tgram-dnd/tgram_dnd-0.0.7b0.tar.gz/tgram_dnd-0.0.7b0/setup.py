from setuptools import setup

setup(
    name="tgram_dnd",
    version="0.0.7beta",
    description="Tgram Darg-And-Drop helper is a lib to help building DragAndDrop applications, or simply just to make bots faster",
    long_description=open("readme.md", "r+").read(),
    long_description_content_type='text/markdown',
    author="SpicyPenguin",
    packages=[
        "tgram_dnd",
        "tgram_dnd.blocks",
        "tgram_dnd.actions",
        "tgram_dnd.actions.api",
        "tgram_dnd.actions.api.methods",
        "tgram_dnd.caching",
        "tgram_dnd.conditions",
        "tgram_dnd.enums",
        "tgram_dnd.flows"
    ],
    install_requires=["jinja2", "tgram"]
)