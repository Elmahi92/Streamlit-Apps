import json
import streamlit as st

from pathlib import Path
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace
from streamlit_elements import mui

from dashboard import Dashboard, HeaderCard, Editor, KPI_Card, DataGrid, Radar, Pie, Player  # Use KPI_Card here

def main():
    #st.write("✨ Streamlit Elements Demo ✨")
    #st.title("")  # You can set a title here if needed

    if "w" not in state:
        board = Dashboard()

        # Define all widgets including the KPI card
        w = SimpleNamespace(
            dashboard=board,
            editor=Editor(board, 0, 0, 6, 11, minW=3, minH=3),
            player=Player(board, 0, 12, 6, 10, minH=5),
            pie=Pie(board, 6, 0, 6, 7, minW=3, minH=4),
            radar=Radar(board, 12, 7, 3, 7, minW=2, minH=4),
            card1=KPI_Card(board, 0, 0, 4, 2, minW=2, minH=4),  # First KPI card
            data_grid=DataGrid(board, 6, 13, 6, 7, minH=4),
            header_card=HeaderCard(board, 0, 10, 6, 3, minW=3, minH=2)  # Use your dimensions
        )

        # Assign to state.w to persist
        state.w = w

        # Add content to each card's editor tab using fixed strings
        w.editor.add_tab("Card 1 content", "This is the default content for Card 1.", "plaintext")
        w.editor.add_tab("Data grid", json.dumps(DataGrid.DEFAULT_ROWS, indent=2), "json")
        w.editor.add_tab("Radar chart", json.dumps(Radar.DEFAULT_DATA, indent=2), "json")
        w.editor.add_tab("Pie chart", json.dumps(Pie.DEFAULT_DATA, indent=2), "json")

    else:
        w = state.w

    with elements("demo"):
        event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)
        
        with w.dashboard(height=100):
            # Render the header card at the top
            w.header_card(
                title="Welcome to the Dashboard",
                subtitle="Overview of Key Metrics",
                body_text="This dashboard provides insights into the latest performance metrics. Please explore the various sections for detailed analysis.",
                media_url="https://media.gettyimages.com/id/1218250907/photo/terrified-black-refugee-muslim-young-woman-because-the-horrors-of-pandemic.jpg?s=612x612&w=0&k=20&c=8WboY31kq0XhDLVrqlAdgyIIslGwintnlAut9HS5zjo=",  # Replace with your media URL
                alt_text="Dashboard Overview Image",
                width=100,
                height=200,
                top=0,  # Positioned at the top
                left=0
            )
            
            # Render the KPI card below the header card
            w.card1(
                content=w.editor.get_content("Card 1 content"),
                title="KPI Title 1",
                subheader="Period: Q1 2024",
                avatar_text="S1",
                avatar_color="blue",
                value="15,000",  # Example KPI value
                trend="up",  # Example trend (up/down)
                width=350,
                height=400,
                top=353,  # Positioned below the header card
                left=0
            )

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
