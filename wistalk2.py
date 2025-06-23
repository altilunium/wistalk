import requests

def get_user_contributions(username: str, lang_code: str) -> dict:
    """
    Fetches all Wikipedia page contributions for a given user in a specific language,
    aggregating the total byte difference for each page.

    Args:
        username (str): The Wikipedia username.
        lang_code (str): The Wikipedia language code (e.g., 'en' for English, 'id' for Indonesian).

    Returns:
        dict: A dictionary where keys are page titles and values are the
              total byte count contributed by the user to that page.
              Returns an empty dictionary if the user has no contributions or an error occurs.
    """
    base_url = f"https://{lang_code}.wikipedia.org/w/api.php"
    all_contributions = {}
    uccontinue = None # For pagination

    print(f"Fetching contributions for user '{username}' on {lang_code.upper()} Wikipedia...")

    while True:
        params = {
            "action": "query",
            "list": "usercontribs",
            "ucuser": username,
            "uclimit": "500", # Max limit per request
            "ucprop": "title|sizediff", # Get page title and byte difference for each edit
            "format": "json",
            "ucshow": "!new", # Exclude 'new page' creations as sizediff for new pages is often zero
                             # and doesn't represent content added. For this task, we focus on actual content diff.
        }
        if uccontinue:
            params["uccontinue"] = uccontinue

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            data = response.json()

            user_contribs = data.get("query", {}).get("usercontribs", [])
            for contrib in user_contribs:
                title = contrib.get("title")
                # sizediff can be negative for removals, positive for additions
                # We are interested in the absolute change, but for "contributed bytes",
                # positive sizediff (additions) is what we count.
                # If a user deletes content, that's still a "touch" but might not
                # count as "contributed bytes" in the positive sense.
                # For this script, we'll sum all sizediff values as they represent
                # the net change the user made.
                size_diff = contrib.get("sizediff", 0)

                if title:
                    all_contributions[title] = all_contributions.get(title, 0) + size_diff

            # Check if there are more results to fetch (pagination)
            if "continue" in data:
                uccontinue = data["continue"].get("uccontinue")
                print(f"  Continuing fetch with: {uccontinue}")
            else:
                break # No more contributions
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")
            return {} # Return empty on error
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return {}

    return all_contributions

def main():
    """
    Main function to get user input, fetch contributions, and display sorted results.
    """
    wikipedia_username = input("Enter Wikipedia username: ")
    wikipedia_language_code = input("Enter Wikipedia language code (e.g., 'en', 'id', 'fr'): ").lower()

    if not wikipedia_username or not wikipedia_language_code:
        print("Username and language code cannot be empty.")
        return

    # Fetch contributions
    contributions = get_user_contributions(wikipedia_username, wikipedia_language_code)

    if not contributions:
        print(f"\nNo contributions found for '{wikipedia_username}' on {wikipedia_language_code.upper()} Wikipedia, or an error occurred.")
        return

    # Sort contributions by byte count (descending)
    # We convert to a list of tuples for sorting, then back to a dictionary for display.
    sorted_contributions = sorted(contributions.items(), key=lambda item: item[1], reverse=True)

    print(f"\n--- Contributions for '{wikipedia_username}' on {wikipedia_language_code.upper()} Wikipedia (Sorted by Byte Count) ---")
    for title, byte_count in sorted_contributions:
        # Filter out pages where net contribution is zero, as they don't represent significant "touches"
        if byte_count != 0:
            print(f"Page: {title:<50} | Contributed Bytes: {byte_count:,}")

    print("\nNote: 'Contributed Bytes' represents the net change in byte count made by the user to the page.")
    print("      A positive number indicates additions, a negative number indicates removals.")


if __name__ == "__main__":
    main()
