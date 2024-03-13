from geotext.geotext import GeoText

def main():
    places = GeoText("London is a great city")
    print(f"Cities mentioned: {places.cities}")
    # Output: Cities mentioned: ['London']

    result = GeoText('I loved Rio de Janeiro and Havana', 'BR').cities
    print(f"Cities in Brazil: {result}")
    # Output: Cities in Brazil: ['Rio de Janeiro']

    country_mentions = GeoText('New York, Texas, and also China').country_mentions
    print(f"Country mentions: {country_mentions}")
    # Output: Country mentions: OrderedDict([('US', 2), ('CN', 1)])

if __name__ == "__main__":
    main()
