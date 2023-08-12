# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pymongo
client=pymongo.MongoClient("mongodb://localhost:27017")
DB=client["Canteen"]
TRajColl=DB["Yamuna"]
class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        breakFast = TRajColl.find({"_id":1})
        c=1
        for i in breakFast:
            item = i["item"+str(c)]
            dispatcher.utter_message(item)
            c=c+1
            
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

class ActionSetChosenCanteen(Action):
    def name(self) -> Text:
        return "action_set_chosen_canteen"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        chosen_canteen = next(tracker.get_latest_entity_values("canteen_name"), None)
        
        if chosen_canteen:
            dispatcher.utter_message(text="Great choice! You've chosen the {} Canteen for your order.".format(chosen_canteen))
            return [SlotSet("chosen_canteen", chosen_canteen)]
        else:
            dispatcher.utter_message(text="I'm sorry, I didn't catch which canteen you chose.")
            return []

