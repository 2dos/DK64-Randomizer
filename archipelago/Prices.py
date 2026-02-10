"""Shop price generation functionality for Archipelago DK64."""

from randomizer.Enums.Items import Items as DK64RItems
from randomizer.Lists.Item import ItemList as DK64RItemList
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Types import Types
from randomizer.Lists.Location import SharedShopLocations

class PriceGenerator:
    """Generates custom shop prices for Archipelago DK64."""

    # Progressive moves configuration (item: count)
    PROGRESSIVE_MOVES = {
        "ProgressiveSlam": 3,
        "ProgressiveAmmoBelt": 2,
        "ProgressiveInstrumentUpgrade": 3,
    }

    def __init__(self, spoiler, options, random):
        """Initialize the price generator."""
        self.spoiler = spoiler
        self.options = options
        self.random = random

    def _get_price_weights(self, shop_prices_value):
        """Get the parameters for the price distribution."""
        match shop_prices_value:
            case 3:  # Hard
                return (6.5, 3, 12)
            case 2:  # Medium
                return (4.5, 2, 9)
            case 1:  # Easy
                return (2.5, 1, 6)
            case _:  # Free
                return (0, 0, 0)

    def _generate_random_price(self, avg, stddev, upper_limit):
        """Generate a random price using normal distribution."""
        if avg == 0:  # Free prices
            return 0

        price = round(self.random.normalvariate(avg, stddev))
        return max(1, min(price, upper_limit))

    def _get_shared_shop_vendors(self, Kongs, Types):
        """Identify vendor/level combinations that have shared shops."""

        shared_shop_vendors = set()

        if not self.options.enable_shared_shops.value:
            if not hasattr(self.spoiler.settings, "selected_shared_shops"):
                self.spoiler.settings.selected_shared_shops = set()
            return shared_shop_vendors, set()

        # Get or create the set of available shared shops
        if hasattr(self.spoiler.settings, "selected_shared_shops") and self.spoiler.settings.selected_shared_shops:
            available_shared_shops = self.spoiler.settings.selected_shared_shops
        else:
            all_shared_shops = list(SharedShopLocations)
            self.random.shuffle(all_shared_shops)
            available_shared_shops = set(all_shared_shops[:10])
            self.spoiler.settings.selected_shared_shops = available_shared_shops

        # Build set of vendor/level combinations
        for location_id, location in self.spoiler.LocationList.items():
            if location.type == Types.Shop and location.kong == Kongs.any:
                if location_id in available_shared_shops:
                    shared_shop_vendors.add((location.level, location.vendor))

        return shared_shop_vendors, available_shared_shops

    def _categorize_shop_locations(self, shared_shop_vendors, available_shared_shops, Kongs, Types):
        """Categorize shops into included and excluded based on settings."""
        shop_locations = []
        excluded_shop_locations = []
        shops_per_kong = {kong: 0 for kong in Kongs}

        for location_id, location in self.spoiler.LocationList.items():
            if location.type != Types.Shop:
                continue

            # Check if shop is excluded by smaller_shops setting
            if hasattr(location, "smallerShopsInaccessible") and location.smallerShopsInaccessible and self.options.smaller_shops.value:
                excluded_shop_locations.append(location_id)
                continue

            # Check if shared shop is excluded
            if location.kong == Kongs.any:
                if not self.options.enable_shared_shops.value or location_id not in available_shared_shops:
                    excluded_shop_locations.append(location_id)
                    continue

            # Check if kong shop is blocked by a shared shop at same vendor/level
            if location.kong != Kongs.any and self.options.enable_shared_shops.value:
                if (location.level, location.vendor) in shared_shop_vendors:
                    excluded_shop_locations.append(location_id)
                    continue

            # Shop is included
            shop_locations.append(location_id)
            if location.kong != Kongs.any:
                shops_per_kong[location.kong] += 1

        return shop_locations, excluded_shop_locations, shops_per_kong

    def _generate_individual_prices(self, shop_locations, avg, stddev, upper_limit, DK64RItems):
        """Generate random individual prices for shops and progressive items."""
        individual_prices = {}

        # Generate shop prices - simple random price per shop
        for location_id in shop_locations:
            individual_prices[location_id] = self._generate_random_price(avg, stddev, upper_limit)

        # Progressive items get their own price list
        for item_name, count in self.PROGRESSIVE_MOVES.items():
            item_enum = getattr(DK64RItems, item_name)
            individual_prices[item_enum] = []
            for _ in range(count):
                individual_prices[item_enum].append(self._generate_random_price(avg, stddev, upper_limit))

        return individual_prices

    def _convert_to_cumulative_prices(self, individual_prices, shop_locations, Kongs):
        """Convert individual prices to cumulative running totals per kong."""
        price_assignment = []

        # Build list of price assignments
        for key, value in individual_prices.items():
            if isinstance(value, list):
                # Progressive move - add multiple entries
                for price in value:
                    price_assignment.append({"is_prog": True, "cost": price, "item": key, "kong": Kongs.any})
            elif key in shop_locations:
                # Shop location
                location = self.spoiler.LocationList[key]
                price_assignment.append({"is_prog": False, "cost": value, "item": key, "kong": location.kong})

        # Shuffle and calculate cumulative prices
        self.random.shuffle(price_assignment)
        total_cost = [0] * 5
        cumulative_prices = {}

        for assignment in price_assignment:
            kong = assignment["kong"]
            written_price = assignment["cost"]

            if kong == Kongs.any:
                # Progressive item - add to all kongs, price is average of current totals
                current_kong_total = 0
                for kong_index in range(5):
                    current_kong_total += total_cost[kong_index]
                    total_cost[kong_index] += written_price
                written_price = int(current_kong_total / 5)
            else:
                # Kong-specific shop - add to that kong's total
                total_cost[kong] += written_price
                written_price = total_cost[kong]

            # Store cumulative price
            key = assignment["item"]
            if assignment["is_prog"]:
                if key not in cumulative_prices:
                    cumulative_prices[key] = []
                cumulative_prices[key].append(written_price)
            else:
                cumulative_prices[key] = written_price

        return cumulative_prices

    def generate_prices(self):
        """Generate custom shop prices for Archipelago."""
        # Get price distribution parameters (matches standalone)
        shopprices = self.options.shop_prices.value
        avg, stddev, upper_limit = self._get_price_weights(shopprices)

        # Categorize shops
        shared_shop_vendors, available_shared_shops = self._get_shared_shop_vendors(Kongs, Types)
        shop_locations, excluded_shop_locations, shops_per_kong = self._categorize_shop_locations(shared_shop_vendors, available_shared_shops, Kongs, Types)

        # Generate individual prices using standalone algorithm
        individual_prices = self._generate_individual_prices(shop_locations, avg, stddev, upper_limit, DK64RItems)

        # Add 0 prices for non-shop items and excluded shops
        for item_id in DK64RItemList.keys():
            if item_id not in individual_prices:
                individual_prices[item_id] = 0

        for location_id in excluded_shop_locations:
            individual_prices[location_id] = 0

        # Store original prices
        self.spoiler.settings.original_prices = individual_prices.copy()

        if shopprices > 0:
            # Convert to cumulative prices
            cumulative_prices = self._convert_to_cumulative_prices(individual_prices, shop_locations, Kongs)

            # Add 0 prices for items not in shops
            for item_id in DK64RItemList.keys():
                if item_id not in cumulative_prices:
                    cumulative_prices[item_id] = 0

            # Add 0 prices for all location IDs not already priced
            for location_id in self.spoiler.LocationList.keys():
                if location_id not in cumulative_prices:
                    cumulative_prices[location_id] = 0

            for location_id in excluded_shop_locations:
                cumulative_prices[location_id] = 0

            self.spoiler.settings.prices = cumulative_prices
        else:
            # Free prices - ensure all locations exist with 0 cost
            for location_id in self.spoiler.LocationList.keys():
                if location_id not in individual_prices:
                    individual_prices[location_id] = 0
            self.spoiler.settings.prices = individual_prices.copy()
