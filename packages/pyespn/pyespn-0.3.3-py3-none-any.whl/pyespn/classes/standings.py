from pyespn.core.decorators import validate_json
from pyespn.utilities import fetch_espn_data
from pyespn.classes.player import Player
from pyespn.classes.team import Manufacturer
from pyespn.classes.stat import Record


@validate_json("standings_json")
class Standings:
    """
    Represents the standings for a racing league, including athletes, manufacturers, and performance records.

    This class initializes and processes standings data from a given JSON structure, fetching
    additional details for athletes and manufacturers via the ESPN API.

    Attributes:
        standings_json (dict): Raw JSON data containing the standings structure.
        espn_instance (object): An instance of the ESPN API handler (PyESPN).
        standings (list): A list of dictionaries, each containing:
            - 'athlete' (Player or None): The athlete in the standing.
            - 'manufacturer' (Manufacturer or None): The associated manufacturer.
            - 'record' (list of Record): A list of performance records.
        standings_type_name (str): The display name for the standings category (e.g., "Drivers", "Constructors").
        this_athlete (Player or None): Temporary reference to the currently processed athlete.
        this_manufacturer (Manufacturer or None): Temporary reference to the currently processed manufacturer.

    Methods:
        __repr__(): Returns a string representation of the standings.
        _load_standings_data(): Parses JSON and populates the standings with athletes, manufacturers, and records.
    """

    def __init__(self, standings_json, espn_instance):
        """
        Initializes the Standings instance and loads standings data.

        Args:
            standings_json (dict): The JSON data containing standings information.
            espn_instance (object): An instance of the ESPN API handler.
        """

        self.standings_json = standings_json
        self._espn_instance = espn_instance
        self.standings = []
        self._load_standings_data()

    def __repr__(self) -> str:
        """
        Returns a string representation of the Standings instance.

        The representation includes the standings type and the number of entries in the standings list.

        Returns:
            str: A formatted string representing the standings.
        """
        return f"<Standings | {self.standings_type_name}, Entries: {len(self.standings)}>"

    def _load_standings_data(self):
        """
        Parses the standings JSON and populates the standings attribute.

        This method extracts relevant standings information, including details about athletes,
        manufacturers, and their performance records. It fetches additional data from ESPN APIs
        as needed to populate Player and Manufacturer objects.

        Populates:
            standings (list): A list of dictionaries, each containing:
                - 'athlete' (Player or None): The athlete associated with the standing.
                - 'manufacturer' (Manufacturer or None): The manufacturer associated with the standing.
                - 'record' (list of Record objects): Performance records for the athlete or manufacturer.
        """

        this_athlete = None
        this_manufacturer = None
        self.standings_type_name = self.standings_json.get('displayName')
        for competitor in self.standings_json.get('standings', []):
            if 'athlete' in competitor:
                athlete_content = fetch_espn_data(competitor.get('athlete', {}).get('$ref'))
                this_athlete = Player(player_json=athlete_content,
                                      espn_instance=self._espn_instance)
            elif 'manufacturer' in competitor:
                manufacturer_content = fetch_espn_data(competitor.get('manufacturer', {}).get('$ref'))
                this_manufacturer = Manufacturer(manufacturer_json=manufacturer_content,
                                                 espn_instance=self._espn_instance)
            records = []
            for record in competitor.get('records', []):
                records.append(Record(record_json=record,
                                      espn_instance=self._espn_instance))
            full_athlete = {
                'athlete': this_athlete,
                'manufacturer': this_manufacturer,
                'record': records
            }

            self.standings.append(full_athlete)

    @property
    def espn_instance(self):
        """
            PYESPN: the espn client instance associated with the class
        """
        return self._espn_instance

    def to_dict(self) -> dict:
        """
        Converts the Standings instance to its original JSON dictionary.

        Returns:
            dict: The standings's raw JSON data.
        """
        return self.standings_json
