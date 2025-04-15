from pyespn.core.decorators import validate_json
from pyespn.classes.vehicle import Vehicle
from pyespn.classes.event import Event
from pyespn.classes.image import Image
from pyespn.classes.stat import StatCategory
from pyespn.utilities import fetch_espn_data, get_an_id


@validate_json('player_json')
class Player:
    from pyespn.core.orchestration import get_players_historical_stats_core
    """
    Represents a player within the ESPN API framework.

    This class stores player-related information and maintains a reference
    to a `PYESPN` instance, allowing access to league-specific details.

    Attributes:
        espn_instance (PYESPN): The parent `PYESPN` instance providing access to league details.
        player_json (dict): The raw player data retrieved from the ESPN API.
        api_ref (str | None): API reference link for the player.
        id (str | None): The unique identifier for the player.
        uid (str | None): The ESPN UID for the player.
        guid (str | None): The GUID associated with the player.
        type (str | None): The type of player (e.g., 'athlete').
        flag (dict | None): The player's flag data (for nationality, mainly in racing).
        citizenship (str | None): The player's citizenship code.
        experience (dict | int | None): Raw experience data from API.
        experience_years (int | None): Number of years of experience.
        event_log (dict | None): Reference to player's event log.
        stats_log (dict | None): Raw statistics log.
        alternate_ids (str | None): Alternate ID, e.g., SDR ID.
        first_name (str | None): The player’s first name.
        last_name (str | None): The player’s last name.
        full_name (str | None): The player’s full name.
        display_name (str | None): Display name.
        short_name (str | None): Shortened name.
        weight (int | None): Weight in pounds.
        display_weight (str | None): Formatted display weight.
        height (int | None): Height in inches.
        display_height (str | None): Formatted display height.
        age (int | None): Age.
        date_of_birth (str | None): Date of birth (YYYY-MM-DD).
        debut_year (int | None): Debut year.
        college_athlete_ref (str | None): Ref to the college athlete profile.
        links (list[dict]): Related links for the player.
        birth_city (str | None): City of birth.
        birth_state (str | None): State of birth.
        college_ref (str | None): College reference.
        slug (str | None): URL slug for the player.
        jersey (str | None): Jersey number.
        position_ref (str | None): API reference for position.
        position_id (str | None): Position ID.
        position_name (str | None): Full position name.
        position_display_name (str | None): Position display label.
        position_abbreviation (str | None): Position abbreviation (e.g., "QB").
        position_leaf (bool | None): Whether it's a leaf node in hierarchy.
        position_parent_ref (str | None): Reference to parent position node.
        linked (str | None): Linked player info, if available.
        team_ref (str | None): Ref to current team.
        statistics_ref (str | None): Ref to statistical summary.
        contracts_ref (str | None): Ref to contract data.
        active (bool | None): Whether the player is active.
        status_id (str | None): Status ID.
        status_name (str | None): Status name.
        status_type (str | None): Status type (e.g., "Active", "Injured").
        status_abbreviation (str | None): Abbreviation of status.
        statistics_log_ref (str | None): Ref to full stat log.
        vehicles (list[Vehicle] | None): List of vehicles (racing-specific).
        stats (dict): Historical statistics loaded via `load_player_historical_stats()`.

    Methods:
        __repr__() -> str:
            Returns a string representation of the Player instance, including full name, position abbreviation, and jersey number.

        _set_player_data() -> None:
            Internal method that parses and assigns player data from the provided JSON.

        load_player_historical_stats() -> None:
            Loads the historical statistics for the player and stores them in the `stats` attribute.

        to_dict() -> dict:
            Returns the raw player JSON data as a dictionary.
    """

    def __init__(self, espn_instance, player_json: dict):
        """
        Initializes a Player instance.

        Args:
            espn_instance (PYESPN): The parent `PYESPN` instance, providing access to league details.
            player_json (dict): The raw player data retrieved from the ESPN API.
        """
        self.player_json = player_json
        self._espn_instance = espn_instance
        self.api_info = self._espn_instance.api_mapping
        self._stats = {}
        self._stats_game_log = {}
        self._set_player_data()
        
    @property
    def espn_instance(self):
        """
            PYESPN: the espn client instance associated with the class
        """
        return self._espn_instance
    
    @property
    def stats_game_log(self):
        """
            dict: with season as a key and has a list of StatCategory Objects
        """
        return self._stats_game_log

    @property
    def stats(self):
        """
            dict: with season as key with list of Stats Objects
        """
        return self._stats

    @property
    def id(self):
        """
            str: the id for the player
        """
        return self._id

    def __repr__(self) -> str:
        """
        Returns a string representation of the Player instance.

        Returns:
            str: A formatted string with the players's name, position and jersey.
        """
        return f"<Player | {self.full_name}, {self.position_abbreviation} ({self.jersey})>"

    def _set_player_data(self):
        """
        Extracts and sets player data from the provided JSON.
        """
        self.api_ref = self.player_json.get('$ref')
        self._id = self.player_json.get('id')
        self.uid = self.player_json.get('uid')
        self.guid = self.player_json.get('guid')
        self.type = self.player_json.get('type')
        self.flag = self.player_json.get('flag')
        self.citizenship = self.player_json.get('citizenship')
        self.experience = self.player_json.get('experience')
        self.event_log = self.player_json.get('eventLog')
        self.stats_log = self.player_json.get('statisticslog')
        self.alternate_ids = self.player_json.get('alternateIds', {}).get('sdr')
        self.first_name = self.player_json.get('firstName')
        self.last_name = self.player_json.get('lastName')
        self.full_name = self.player_json.get('fullName')
        if not self.full_name:
            self.full_name = self.first_name + ' ' + self.last_name
        self.display_name = self.player_json.get('displayName')
        self.short_name = self.player_json.get('shortName')
        self.weight = self.player_json.get('weight')
        self.display_weight = self.player_json.get('displayWeight')
        self.height = self.player_json.get('height')
        self.display_height = self.player_json.get('displayHeight')
        self.age = self.player_json.get('age')
        self.date_of_birth = self.player_json.get('dateOfBirth')
        self.debut_year = self.player_json.get('debutYear')
        self.college_athlete_ref = self.player_json.get('collegeAthlete', {}).get('$ref')

        self.links = self.player_json.get('links', [])

        birth_place = self.player_json.get('birthPlace', {})
        self.birth_city = birth_place.get('city')
        self.birth_state = birth_place.get('state')

        self.college_ref = self.player_json.get('college', {}).get('$ref')
        self.slug = self.player_json.get('slug')
        self.jersey = self.player_json.get('jersey', '--')

        position = self.player_json.get('position', {})
        self.position_ref = position.get('$ref')
        self.position_id = position.get('id')
        self.position_name = position.get('name')
        self.position_display_name = position.get('displayName')
        self.position_abbreviation = position.get('abbreviation')
        self.position_leaf = position.get('leaf')
        self.position_parent_ref = position.get('parent', {}).get('$ref')

        self.linked = self.player_json.get('linked')
        self.team_ref = self.player_json.get('team', {}).get('$ref')
        self.statistics_ref = self.player_json.get('statistics', {}).get('$ref')
        self.contracts_ref = self.player_json.get('contracts', {}).get('$ref')

        experience = self.player_json.get('experience', {})
        if type(experience) == dict:
            self.experience_years = experience.get('years')
        elif type(experience) == int:
            self.experience_years = experience

        self.active = self.player_json.get('active')

        status = self.player_json.get('status', {})
        self.status_id = status.get('id')
        self.status_name = status.get('name')
        self.status_type = status.get('type')
        self.status_abbreviation = status.get('abbreviation')

        self.headshot = self.player_json.get('headshot')
        if self.headshot:
            self.headshot = Image(image_json=self.headshot,
                                  espn_instance=self._espn_instance)
        self.statistics_log_ref = self.player_json.get('statisticslog', {}).get('$ref')

        if 'vehicles' in self.player_json:
            self.vehicles = []
            for vehicle in self.player_json.get('vehicles'):
                self.vehicles.append(Vehicle(vehicle_json=vehicle,
                                             espn_instance=self._espn_instance))

    def load_player_historical_stats(self) -> None:
        """
        Loads the historical statistics for the player.

        This method fetches and assigns the player's historical stats using the ESPN API.
        The stats are stored in the `self._stats` attribute.

        Returns:
            None
        """

        self._stats = self.get_players_historical_stats_core(player_id=self._id,
                                                             league_abbv=self._espn_instance.league_abbv,
                                                             espn_instance=self._espn_instance)

    def load_player_box_scores_season(self, season):
        """
        Loads the player's box score statistics for every game in the given season.

        This method fetches the event log for a player for a specific season using ESPN's API.
        It iterates through each event (game) the player participated in, retrieves the game event data,
        and corresponding statistics, then stores it in the player's `_stats_game_log` cache.

        Args:
            season (int): The season year to load player game-by-game statistics for.

        Side Effects:
            Populates the `_stats_game_log` dictionary with a list of game stat dictionaries for the given season.
            Each entry in the list is a dictionary containing:
                - 'event' (`Event`): The event object representing the game.
                - 'stats' (List[`StatCategory`]): A list of stat category objects for that game.
        """
        url = f'http://sports.core.api.espn.com/{self._espn_instance.v}/sports/{self.api_info["sport"]}/leagues/{self.api_info["league"]}/seasons/{season}/athletes/{self._id}/eventlog'
        page_content = fetch_espn_data(url)
        pages = page_content.get('events', {}).get('pageCount', 0)

        event_list = []
        for page in range(1, pages + 1):
            paged_url = url + f'?page={page}'
            event_log_content = fetch_espn_data(paged_url)
            for event_log in event_log_content.get('events', {}).get('items', []):
                event_list.append(event_log)

        event_stats_log = []
        for event in event_list:
            event_id = get_an_id(event.get('event', {}).get('$ref'), 'events')
            event_find = self._espn_instance.league.get_event_by_season(season=season,
                                                                       event_id=event_id)
            if not event_find:
                event_content = fetch_espn_data(event.get('event', {}).get('$ref'))
                event_find = Event(event_json=event_content,
                                   espn_instance=self._espn_instance)
            stats = []
            if event.get('played'):
                stats_content = fetch_espn_data(event.get('statistics', {}).get('$ref'))

                for category in stats_content.get('splits', {}).get('categories'):
                    stats.append(StatCategory(record_json=category,
                                              espn_instance=self._espn_instance))
            event_record = {
                'event': event_find,
                'stats': stats,
            }
            event_stats_log.append(event_record)

        self._stats_game_log[season] = event_stats_log

    def load_player_contracts(self):
        # todo i haven't seen this filled in at all yet in the api
        url = f'http://sports.core.api.espn.com/{self._espn_instance.v}/sports/football/leagues/nfl/athletes/4360807/contracts?lang=en&region=us'

    def to_dict(self) -> dict:
        """
        Returns the raw player JSON data as a dictionary.

        Returns:
            dict: The original player data retrieved from the ESPN API.
        """
        return self.player_json


@validate_json("recruit_json")
class Recruit:
    """
    Represents a recruit in the ESPN recruiting system.

    Attributes:
        recruit_json (dict): The JSON data containing recruit details.
        espn_instance: The ESPN API instance.
        api_ref (str): API reference URL for the recruit.
        athlete (dict): Dictionary containing athlete details.
        id (str): The recruit's unique identifier.
        uid (str): The unique identifier for the recruit.
        guid (str): The global unique identifier.
        type (str): Type of recruit data.
        alternate_ids (str): Alternative ID for the recruit.
        first_name (str): First name of the recruit.
        last_name (str): Last name of the recruit.
        full_name (str): Full name of the recruit.
        display_name (str): Display name of the recruit.
        short_name (str): Shortened version of the recruit's name.
        weight (int): The recruit's weight in pounds (if available).
        height (int): The recruit's height in inches (if available).
        recruiting_class (str): The recruiting class year.
        grade (str): Grade assigned to the recruit.
        links (list): A list of links related to the recruit.
        birth_city (str): City where the recruit was born.
        birth_state (str): State where the recruit was born.
        high_school_id (str): The recruit's high school ID.
        high_school_name (str): Name of the recruit's high school.
        high_school_state (str): State where the recruit's high school is located.
        slug (str): A unique slug identifier for the recruit.
        position_ref (str): API reference for the recruit's position.
        position_id (str): The recruit's position ID.
        position_name (str): Name of the recruit's position.
        position_display_name (str): Display name of the position.
        position_abbreviation (str): Abbreviated name of the recruit's position.
        position_leaf (bool): Whether the position is a leaf node in the hierarchy.
        position_parent_ref (str): Reference to the parent position (if any).
        linked (dict): Additional linked data related to the recruit.
        schools (list): A list of schools associated with the recruit.
        status_id (str): The ID representing the recruit's status.
        status_name (str): Description of the recruit's status.
        rank (int or None): The recruit's overall rank, extracted from attributes.

    Methods:
        __repr__():
            Returns a string representation of the recruit instance.

        _set_recruit_data():
            Extracts and sets player data from the provided JSON.
    """

    def __init__(self, recruit_json: dict, espn_instance):
        """
        Initializes a Recruit instance.

        Args:
            recruit_json (dict): The JSON data containing recruit details.
            espn_instance (PYESPN): The ESPN API instance.
        """
        self.recruit_json = recruit_json
        self._espn_instance = espn_instance
        self._set_recruit_data()

    def __repr__(self) -> str:
        """
        Returns a string representation of the Recruit instance.

        Returns:
            str: A formatted string with the recruits's name, debut year and jersey.
        """
        return f"<Recruit | {self.full_name}, {self.position_abbreviation} ({self.recruiting_class})>"

    def _set_recruit_data(self):
        """
        Extracts and sets recruit data from the provided JSON.
        """
        self.api_ref = self.recruit_json.get('$ref')
        self.athlete = self.recruit_json.get('athlete')
        self._id = self.athlete.get('id')
        self.uid = self.recruit_json.get('uid')
        self.guid = self.recruit_json.get('guid')
        self.type = self.recruit_json.get('type')
        self.alternate_ids = self.athlete.get('alternateIds', {}).get('sdr')
        self.first_name = self.athlete.get('firstName')
        self.last_name = self.athlete.get('lastName')
        self.full_name = self.athlete.get('fullName')
        self.display_name = self.athlete.get('displayName')
        self.short_name = self.athlete.get('shortName')
        self.weight = self.athlete.get('weight')
        self.height = self.athlete.get('height')
        self.recruiting_class = self.recruit_json.get("recruitingClass")
        self.grade = self.recruit_json.get('grade')

        self.links = self.recruit_json.get('links', [])

        birth_place = self.athlete.get('hometown', {})
        self.birth_city = birth_place.get('city')
        self.birth_state = birth_place.get('state')

        high_school = self.athlete.get('highSchool', {})
        self.high_school_id = high_school.get('id')
        self.high_school_name = high_school.get('name')
        self.high_school_state = high_school.get('address', {}).get('state')

        self.slug = self.recruit_json.get('slug')

        position = self.athlete.get('position', {})
        self.position_ref = position.get('$ref')
        self.position_id = position.get('id')
        self.position_name = position.get('name')
        self.position_display_name = position.get('displayName')
        self.position_abbreviation = position.get('abbreviation')
        self.position_leaf = position.get('leaf')
        self.position_parent_ref = position.get('parent', {}).get('$ref')

        self.linked = self.recruit_json.get('linked')
        self.schools = self.recruit_json.get('schools')

        status = self.recruit_json.get('status', {})
        self.status_id = status.get('id')
        self.status_name = status.get('description')

        self.rank = next((int(attr.get('displayValue')) for attr in self.recruit_json.get('attributes', []) if attr.get("name", '').lower() == "rank"), None)

    @property
    def id(self):
        """
            str: the id for the player
        """
        return self._id

    @property
    def espn_instance(self):
        """
            PYESPN: the espn client instance associated with the class
        """
        return self._espn_instance

    def to_dict(self) -> dict:
        """
        Converts the Recruit instance to its original JSON dictionary.

        Returns:
            dict: The recruit's raw JSON data.
        """
        return self.recruit_json
